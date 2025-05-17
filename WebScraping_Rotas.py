# Modulo para controlar o navegador
from selenium import webdriver

# Localizador de elementos
from selenium.webdriver.common.by import By

# Serviço para configurar o caminho do executável chromedriver
from selenium.webdriver.chrome.service import Service

# Classe que permite executar ações avançadas, como por exemplo o mover o mouse, o click e arrasta e etc..
from selenium.webdriver.common.action_chains import ActionChains

# Classe que espera de forma explicita até que uma condição seja satisfeita
# Condição (ex: Que um elemento apareça)
from selenium.webdriver.support.ui import WebDriverWait

# Condições esperadas usadas com WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

# Trabalhar com DataFrame
import pandas as pd

# Uso de funções relacionadas ao tempo
import time 

from selenium.common.exceptions import TimeoutException

# Definir o caminho do chromeDriver 
chrome_driver_path = "C:\Program Files\chromedriver-win64\chromedriver-win64\chromedriver.exe" # Onde esta armazenado o caminho do driver 

# configuração ao WebDriver
service = Service(chrome_driver_path) #navegador controlado pelo Selenium
options = webdriver.ChromeOptions() # configura opções do navegador
options.add_argument("--disable-gpu") # evita possíveis erros gráficos
options.add_argument("--window-size=1920,1080") # define uma resolução fixa

# incialização ao WebDriver
driver = webdriver.Chrome(service=service, options=options) # inicialização do navegador

# URl inicial
url_base = "https://masander.github.io/AlimenticiaLTDA/#/transport"
driver.get(url_base)
time.sleep(10) # aguarda 5 segundos para garantir que a pág carregue

nav = driver.find_elements(By.CLASS_NAME, "subpage_button")

# Verifica se o botão de próxima página está presente
try:
    botao_proximo = driver.find_element(By.XPATH, "//button[contains(text(), 'Rotas')]")
    botao_proximo.click()
    time.sleep(3)  # Aguarda após o clique
except Exception as e:
    print("Erro ao clicar no botão 'Próximo':", e)

#criar um dicionário vazio para armazenar 
dic_Rotas = {"Origem": [], "Destino": [], "Distancia_Km": [], "Tipo_Veiculo": []}

pagina = 1

Rotas = driver.find_elements(By.XPATH, "//table/tbody//tr")

for rota in Rotas:
        try:
            Origem = rota.find_element(By.CLASS_NAME, "td_origem").text.strip()
            Destino = rota.find_element(By.CLASS_NAME, "td_destino").text.strip()
            Distancia_Km = rota.find_element(By.CLASS_NAME, "td_distancia_km").text.strip()
            Tipo_Veiculo = rota.find_element(By.CLASS_NAME, "td_tipo_veiculo").text.strip()
            


            print(f"{Origem} - {Destino} - {Distancia_Km} - {Tipo_Veiculo}")

            dic_Rotas["Origem"].append(Origem)
            dic_Rotas["Destino"].append(Destino)
            dic_Rotas["Distancia_Km"].append(Distancia_Km)
            dic_Rotas["Tipo_Veiculo"].append(Tipo_Veiculo)


        except Exception as e:
            print(Origem)
            print("Erro ao coletar dados:", e)


# Fechar o navegador
driver.quit()

# DataFrame
df = pd.DataFrame(dic_Rotas)

# Salvar os dados em excel
df.to_excel("Rotas.xlsx", index= False)
        