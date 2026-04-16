from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os, sys, logging
import subprocess
import time
import json

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "publica_log.txt")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)


options = Options()
options.add_argument("--disable-infobars")
options.add_argument("--disable-gpu")
options.add_argument("--disable-software-rasterizer")
options.add_argument("--disable-extensions")
options.add_argument("--disable-notifications")
options.add_argument("--no-sandbox")
options.add_argument("--disable-features=VizDisplayCompositor")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-first-run")
options.add_experimental_option("detach", True)

try:
    driver_path = ChromeDriverManager().install()
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    logging.info("ChromeDriver iniciado com sucesso via webdriver_manager!")
except Exception:
    logging.error("Erro ao inicializar o ChromeDriver via webdriver_manager", exc_info=True)
    sys.exit(1)

driver.implicitly_wait(1)
wait = WebDriverWait(driver, 10)



def encontrar_elemento(xpath):
    for _ in range(3):
        try:
            return wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        except Exception:
            time.sleep(2)
    logging.error("Elemento não encontrado: " + xpath)
    raise


def pegarChave():
    
    try:
        return sys.argv[1]
    except IndexError:
        logging.error("Caminho do JSON não informado no argumento 1")
        sys.exit(1)


try:
    if __name__ == "__main__":
        chave = pegarChave()
        with open(chave, 'r', encoding='utf-8') as arquivo:
            try:
                dados = json.load(arquivo)
                logging.info("JSON lido com sucesso")
            except Exception as e:
                logging.error("Erro lendo JSON: " + str(e))
                sys.exit(1)

        email = dados['dadosDeLogin']['email']
        senha = dados['dadosDeLogin']['senha']
        titulo = dados['publicacao']['titulo']
        publicacao = dados['publicacao']['publicacao']

        driver.get("https://br.linkedin.com/")
except Exception as e:
    logging.error("Falha ao abrir JSON ou navegar: " + str(e))
    sys.exit(1)


try:
    selecionarEmailBt = encontrar_elemento("//a[@data-test-id='home-hero-sign-in-cta']")
    selecionarEmailBt.click()
    time.sleep(2.5)

    emailInput = encontrar_elemento("//input[@id='username' and @name='session_key' and @aria-label='E-mail ou telefone']")
    time.sleep(2.5)
    emailInput.send_keys(email)
    time.sleep(0.8)

    senhaInput = encontrar_elemento("//input[@id='password' and @name='session_password' and @aria-label='Senha' and @type='password']")
    time.sleep(2.5)
    senhaInput.send_keys(senha)

    loginBt = encontrar_elemento("//button[@aria-label='Entrar' and @type='submit' and @data-litms-control-urn='login-submit']")
    time.sleep(2.5)
    loginBt.click()

    iniciarPublicacao = encontrar_elemento("//button[@id='ember35' or @class='artdeco-button artdeco-button--muted artdeco-button--4 artdeco-button--tertiary ember-view cTGyaJnGoWfkJLPQELApNvsznXilrNuiMhUpR' or @id='ember34']")
    time.sleep(2)
    iniciarPublicacao.click()

    publicacaoConteudo = encontrar_elemento("//div[@aria-label='Editor de texto para criação de conteúdo' and @role='textbox']")
    publicacaoConteudo.click()
    time.sleep(2.5)
    publicacaoConteudo.send_keys(titulo)
    time.sleep(2.3)
    publicacaoConteudo.send_keys(Keys.ENTER)
    time.sleep(3)
    publicacaoConteudo.send_keys(Keys.ENTER)
    time.sleep(2.4)

    publicacaoConteudo.send_keys(publicacao)
    time.sleep(2)

    botao_enviar_publicacao = encontrar_elemento("//div[@class='share-box_actions']/button")
    time.sleep(2.4)
    botao_enviar_publicacao.click()

    logging.info("Publicação enviada com sucesso!")

    try:
        apagar_tarefa = f'schtasks /Delete /TN "{titulo}" /F'
        resultado = subprocess.run(apagar_tarefa, shell=True, capture_output=True, text=True)
        if resultado.returncode == 0:
            logging.info("Tarefa removida do sistema")
    except Exception as e:
        logging.error("Falha ao tentar remover tarefa: " + str(e))

except Exception as e:
    logging.error("Erro no fluxo Selenium: " + str(e))
    sys.exit(1)
