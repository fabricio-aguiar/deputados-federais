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
    txt = txt.upper()
    return normalize('NFKD', txt).encode('ASCII','ignore').decode('ASCII')


print("\nBens Deputados")

options = Options()
options.add_argument("--start-maximized")


browser = webdriver.Chrome(chrome_options=options)

lista = []# lista = [['Nome', 'Nome para Urna', 'Numero', 'Sexo', 'Estado Civil', 'Ocupacao', 'Cor/Raça', 'Data Nasc.', 'Idade', 'Instrucao', 'Bens', 'UF', 'foto']]

df =  pd.read_csv('Resultado_da_Eleicao.csv',encoding='latin1',sep=';')
df.rename(columns={'Candidato':'Nome Completo'}, inplace=True)
df.drop(['UF'], axis=1,inplace=True) 


dados = pd.read_csv('Detalhes_Deputados.csv',encoding='latin1')
dados2 = pd.read_csv('Atuacao_Deputados.csv',encoding='latin1', sep= ";")

dados.rename(columns={'Nome':'Nome Completo'}, inplace=True)
dados['Nome Completo'] = dados['Nome Completo'].apply(lambda x: remover_acentos(x))

dados2.rename(columns={'Nome':'Nome Completo'}, inplace=True)
dados2['Nome Completo'] = dados['Nome Completo'].apply(lambda x: remover_acentos(x))

dados = dados2.merge(dados,on='Nome Completo')
print(list(set(dados2['Nome Completo']) - set(dados['Nome Completo'])))
print(len(list(set(dados2['Nome Completo']) - set(dados['Nome Completo']))))

df['Nome Completo'] = df['Nome Completo'].apply(lambda x: remover_acentos(str(x)))
df = dados.merge(df,on='Nome Completo')

print(list(set(dados2['Nome Completo']) - set(df['Nome Completo'])))
print(len(list(set(dados2['Nome Completo']) - set(df['Nome Completo']))))

print(dados.columns)
nomesout = list(set(dados2['Nome Completo']) - set(df['Nome Completo']))
for nome in nomesout:
    uf = dados[dados['Nome Completo'] == nome]['UF'].unique()[0]
    print(uf)
    provisorio = []
    nom = dados[dados['Nome Completo'] == nome]['Nome Parlamentar'].unique()[0]
    provisorio.append(nom)
    if nom != remover_acentos(nom):
        provisorio.append(remover_acentos(nom))
            

# for uf in df['UF'].unique():
    browser.get("http://inter01.tse.jus.br/divulga-cand-2014/eleicao/2014/UF/" + uf +"/candidatos/cargo/6")
    # provisorio = dados[dados['Nome Completo'] == nome] #df[df['UF'] == uf]
    for deputado in provisorio:
        # numero = str(deputado).replace(".0","")
        # if len(numero) < 4:
        #     continue
        for i, char in enumerate(deputado):
            browser.find_element_by_xpath("//*[@id='tbl-candidatos_filter']/label/input").send_keys(char)
            # time.sleep(0.3)
            if len(browser.find_elements_by_xpath('//*[contains(text(), "Deferido")]')) == 1:
                break
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
        provisorio.pop()
        nomeUrna = browser.find_element_by_xpath("/html/body/div/div[4]/table/tbody/tr[1]/td[1]").text
        numero = browser.find_element_by_xpath("/html/body/div/div[4]/table/tbody/tr[1]/td[2]").text 
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
        linha = [nome, nomeUrna, numero, sexo, estCivil, ocupacao, cor, data, idade, instrucao, bem.replace(".",""), uf, foto]
        if linha not in lista:
            lista.append(linha)
        print(linha)
        browser.back()
        


with open ('Bens_Deputados.csv','a', newline='') as file:
    writer=csv.writer(file)
    for row in lista:
        print("Writing :",row)
        writer.writerows([row])
   

browser.close()