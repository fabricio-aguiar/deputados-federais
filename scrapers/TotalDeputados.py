import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd


print("\nTotal Deputados")

options = Options()
options.add_argument("--start-maximized")


browser = webdriver.Chrome(chrome_options=options)


df = pd.read_csv('Detalhes_Deputados.csv', encoding='utf-8', sep=';')

geral = 0
url_part = "http://www.camara.leg.br/internet/deputado/Dep_Lista.asp?Legislatura=55&Partido=QQ&SX=QQ&Todos=None&UF="
for uf in df['UF'].unique():
    browser.get(url_part + uf + "&condic=QQ&forma=lista&nome=&ordem=nome&origem=None")
    texto = browser.find_element_by_xpath('//*[@id="content"]').text
    valor1 = int(texto.split()[1])
    try:
        valor2 = int(texto.split()[5])
    except:
        valor2 = 0
    soma = valor1 + valor2
    geral += soma
    time.sleep(2)
    print(geral)
    browser.back()

browser.close()
