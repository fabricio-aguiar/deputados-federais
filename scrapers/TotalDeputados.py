import time
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from unicodedata import normalize
from string import punctuation
import pandas as pd
import numpy as np
import csv


print("\nTotal Deputados")

options = Options()
options.add_argument("--start-maximized")


browser = webdriver.Chrome(chrome_options=options)



df = pd.read_csv('Detalhes_Deputados.csv',encoding='latin1',sep=';')

geral = 0

for uf in df['UF'].unique():
    browser.get("http://www.camara.leg.br/internet/deputado/Dep_Lista.asp?Legislatura=55&Partido=QQ&SX=QQ&Todos=None&UF=" + uf +"&condic=QQ&forma=lista&nome=&ordem=nome&origem=None")
    texto = browser.find_element_by_xpath('//*[@id="content"]').text
    valor1 = int(texto.split(" ")[1])
    try:
        valor2 = int(texto.split(" ")[5])
    except:
        valor2 = 0
    soma = valor1 + valor2
    geral += soma
    time.sleep(2)
    print(geral)
    browser.back()
    
browser.close()