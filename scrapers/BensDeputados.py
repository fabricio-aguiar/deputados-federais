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


def remover_acentos(txt):
    txt = ''.join([letter for letter in txt if letter not in punctuation])
    return normalize('NFKD', txt).encode('ASCII','ignore').decode('ASCII')


print("\nBens Deputados")

options = Options()
options.add_argument("--start-maximized")


browser = webdriver.Chrome(chrome_options=options)

lista = [['Nome', 'Nome para Urna', 'Numero', 'Sexo', 'Estado Civil', 'Ocupacao', 'Cor/Raça', 'Data Nasc.', 'Idade', 'Instrucao', 'Bens', 'UF', 'foto']]

df =  pd.read_csv('Resultado_da_Eleicao.csv',encoding='latin1',sep=';')
df.rename(columns={'Candidato':'Nome Completo'}, inplace=True)
df.drop(['UF'], axis=1,inplace=True) 

dados = pd.read_csv('Detalhes_Deputados.csv',encoding='latin1')
dados.rename(columns={'Nome':'Nome Completo'}, inplace=True)
dados['Nome Completo'] = dados['Nome Completo'].apply(lambda x: remover_acentos(x))

df['Nome Completo'] = df['Nome Completo'].apply(lambda x: remover_acentos(str(x)))
df = dados.merge(df,on='Nome Completo')

for uf in df['UF'].unique():
    browser.get("http://inter01.tse.jus.br/divulga-cand-2014/eleicao/2014/UF/" + uf +"/candidatos/cargo/6")
    provisorio = df[df['UF'] == uf]
    for deputado in provisorio['Nr'].unique():
        numero = str(deputado).replace(".0","")
        if len(numero) < 4:
            continue
        browser.find_element_by_xpath("//*[@id='tbl-candidatos_filter']/label/input").send_keys(numero)
        try: 
            browser.find_element_by_xpath('//*[contains(text(), "Deferido")]').click() 
            
        except:
            browser.find_element_by_xpath("//*[@id='tbl-candidatos_filter']/label/input").clear()
            continue
        while True:
            try:
                nome = browser.find_element_by_xpath("/html/body/div/div[4]/table/tbody/tr[2]/td[1]").text
                break
            except:
                pass
        nomeUrna = browser.find_element_by_xpath("/html/body/div/div[4]/table/tbody/tr[1]/td[1]").text
        sexo = browser.find_element_by_xpath("/html/body/div/div[4]/table/tbody/tr[2]/td[2]").text
        estCivil = browser.find_element_by_xpath("/html/body/div/div[4]/table/tbody/tr[3]/td[2]").text
        ocupacao = browser.find_element_by_xpath("/html/body/div/div[4]/table/tbody/tr[6]/td[2]").text
        cor = browser.find_element_by_xpath("/html/body/div/div[4]/table/tbody/tr[4]/td").text 
        ano = browser.find_element_by_xpath("/html/body/div/div[4]/table/tbody/tr[3]/td[1]").text
        data = ano
        ano = ano.split("/")[2] 
        idade = 2017 - int(ano)
        instrucao = browser.find_element_by_xpath("/html/body/div/div[4]/table/tbody/tr[6]/td[1]").text
        bem = browser.find_element_by_xpath("//*[@id='tab-bens']/table/tfoot/tr/th[2]").text
        bem = bem.split("$ ")[1]
        foto = browser.find_element_by_xpath("/html/body/div/div[3]/p[1]/img").get_attribute("src")
        foto = foto.split("?")[0]
        lista.append([nome, nomeUrna, numero, sexo, estCivil, ocupacao, cor, data, idade, instrucao, bem.replace(".",""), uf, foto])
        print([nome, nomeUrna, numero, sexo, estCivil, ocupacao, cor, data, idade, instrucao, bem.replace(".",""), uf, foto])
        browser.back()
        


with open ('Bens_Deputados.csv','w', newline='') as file:
    writer=csv.writer(file)
    for row in lista:
        print("Writing :",row)
        writer.writerows([row])
   

browser.close()