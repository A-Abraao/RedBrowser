import argparse
import sys
import os
import json
import subprocess
import logging
import re
from datetime import datetime
from dateutil import parser as date_parser

# === Configuração básica ==================================================
if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PUBLICA_EXE = os.path.join(BASE_DIR, "publica.exe")
LOG_DIR = os.getenv("LOCALAPPDATA", BASE_DIR)
LOG_FILE = os.path.join(LOG_DIR, "agendar_log.txt")
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8",
)

# === Utilidades ===========================================================

def parse_args():
    p = argparse.ArgumentParser(
        description="Agenda a execução do publica.exe via arquivo .bat no Agendador de Tarefas."
    )
    p.add_argument("json_path", help="Caminho para o arquivo JSON da tarefa")
    return p.parse_args()

def load_json(path: str):
    if not os.path.isfile(path):
        logging.error(f"Arquivo JSON não encontrado: {path}")
        sys.exit(1)
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception as exc:
        logging.exception("Falha ao ler JSON", exc_info=exc)
        sys.exit(1)

def sanitize(name: str) -> str:
    """Remove caracteres inválidos e troca espaços por sublinhado."""
    name = re.sub(r'[<>:"/\\|?*]', "_", name)   # proibidos
    return re.sub(r"\s+", "_", name)            # espaços → _

def create_bat(json_path: str, safe_name: str, run_at: datetime) -> str:
    """Gera um .bat exclusivo para a tarefa e devolve seu caminho."""
    bat_name = f"run_publica_{safe_name}_{run_at:%Y%m%d_%H%M}.bat"
    bat_path = os.path.join(BASE_DIR, bat_name)

    bat_lines = [
        "@echo off",
        f'cd /d "{BASE_DIR}"',
        f'"{PUBLICA_EXE}" "{json_path}"',
    ]
    with open(bat_path, "w", encoding="utf-8") as f:
        f.write("\r\n".join(bat_lines))

    logging.info(f"Arquivo BAT criado em {bat_path}")
    return bat_path

def schedule_task(task_name: str, bat_path: str, run_at: datetime):
    """Agenda o .bat no Task Scheduler."""
    date_str = run_at.strftime("%d/%m/%Y")
    time_str = run_at.strftime("%H:%M")

    cmd = [
        "schtasks", "/Create",
        "/SC", "ONCE",
        "/TN", task_name,
        "/TR", bat_path,
        "/SD", date_str,
        "/ST", time_str,
        "/RL", "HIGHEST",   # mantenha se rodar em prompt admin; caso contrário remova
        "/IT",              # sessão interativa (dispensa senha)
        "/F",
    ]

    logging.info("Executando: " + " ".join(f'"{c}"' if " " in c else c for c in cmd))
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        logging.error(f"Agendamento falhou ({result.returncode}): {result.stderr.strip()}")
        sys.exit(result.returncode)

    logging.info(f"Tarefa '{task_name}' agendada para {date_str} {time_str}")

# === Fluxo principal ======================================================

def main():
    args = parse_args()
    dados = load_json(args.json_path)

    pub = dados.get("publicacao", {})
    if not {"titulo", "horario"}.issubset(pub):
        logging.error("JSON inválido: faltam campos em 'publicacao'")
        sys.exit(1)

    titulo      = pub["titulo"]
    horario_iso = pub["horario"]

    try:
        run_at = date_parser.isoparse(horario_iso)
    except Exception as exc:
        logging.error(f"Horário inválido '{horario_iso}': {exc}")
        sys.exit(1)

    if run_at <= datetime.now(run_at.tzinfo):
        logging.error("Horário já passou")
        sys.exit(1)

    safe_name = sanitize(titulo)
    bat_path  = create_bat(args.json_path, safe_name, run_at)
    schedule_task(safe_name, bat_path, run_at)

if __name__ == "__main__":
    main()
