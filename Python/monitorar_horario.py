import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime
import os
import subprocess
import time
import sys
import logging

log_path = os.path.join(os.path.dirname(sys.executable), "monitorar_log.txt")
os.makedirs(os.path.dirname(log_path), exist_ok=True)

logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

tarefa_nome = "AutomatizarPublicacao"
rodar_tarefa = f'schtasks /RUN /TN "{tarefa_nome}"'

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

try:
    cred_path = resource_path("redbrowser-fa70d-firebase-adminsdk-fbsvc-f4cced1181.json")
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://redbrowser-fa70d-default-rtdb.firebaseio.com/'
    })
    logging.info("Firebase inicializado com sucesso.")
except Exception as e:
    logging.critical(f"Falha ao inicializar Firebase: {e}")
    sys.exit(1)

ref = db.reference("/horario")
publica = resource_path("publica.exe")

logging.info(f"Caminho para publica.exe: {publica}")
logging.info(f"publica.exe existe? {os.path.exists(publica)}")

def monitorar_horario():
    hoje = datetime.now().date()
    logging.info("Iniciando monitoramento do horário.")

    while True:
        try:
            horario_str = ref.get()
            logging.debug(f"Horário recebido do Firebase: {horario_str}")

            if horario_str:
                try:
                    horario_meta = datetime.strptime(f"{hoje} {horario_str}", "%Y-%m-%d %H:%M")
                except ValueError:
                    logging.warning(f"Horário inválido recebido do Firebase: {horario_str}")
                    time.sleep(60)
                    continue

                agora = datetime.now()
                if agora >= horario_meta:
                    logging.info(f"Hora alcançada ({horario_meta}), executando tarefa agendada.")
                    subprocess.run(rodar_tarefa, shell=True)
                    logging.info("Tarefa agendada executada, encerrando monitoramento.")
                    break
            else:
                logging.debug("Nenhum horário configurado no Firebase.")

        except Exception as e:
            logging.error(f"Erro ao verificar o horário: {e}")

        time.sleep(2)

    sys.exit(0)

if __name__ == "__main__":
    try:
        monitorar_horario()
    except Exception as e:
        logging.critical(f"Erro fatal no serviço: {e}")
        sys.exit(1)
