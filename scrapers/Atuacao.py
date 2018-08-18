import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import numpy as np
import csv


print("\n Atuacao Deputados")

options = Options()
options.add_argument("--start-maximized")


browser = webdriver.Chrome(chrome_options=options)
browser.get('http://www.camara.leg.br/internet/deputado/pesquisaHistorico.asp')
browser.find_element_by_xpath('//*[@id="dt_inicial"]').send_keys("001022015")
lista = [['Nome', 'Atuacao']]


browser.find_element_by_xpath('//*[@id="filiacaoPartidaria"]').click()
browser.find_element_by_xpath('//*[@id="mudancaNomePart"]').click()
browser.find_element_by_xpath('//*[@id="histLideranca"]').click()
browser.find_element_by_xpath('//*[@id="comisPermanente"]').click()
browser.find_element_by_xpath('//*[@id="comisTemporaria"]').click()

dataset2017 = pd.read_csv('../data/Ano-2017.csv', sep=';',
                          dtype={'idecadastro': np.str})

dataset2016 = pd.read_csv('../data/Ano-2016.csv', sep=';',
                          dtype={'idecadastro': np.str})

dataset2015 = pd.read_csv('../data/Ano-2015.csv', sep=';',
                          dtype={'idecadastro': np.str})


dataset = pd.concat([dataset2017, dataset2016, dataset2015])


for deputado in dataset['txNomeParlamentar'].unique():
    browser.find_element_by_xpath('//*[@id="parlamentar"]').clear()
    browser.find_element_by_xpath('//*[@id="parlamentar"]').send_keys(deputado)
    browser.find_element_by_xpath('//*[@id="form"]/div[3]/input[1]').click()
    time.sleep(1)
    try:
        historico = browser.find_element_by_class_name('panel-body')
    except:
        browser.back()
    continue

    items = historico.find_elements_by_tag_name("li")
    countE = 0
    countS = 0
    atuacao = []

    for n, ocorrencia in enumerate(items):
        if (("Posse()" in ocorrencia.text) or ("Reassunção" in ocorrencia.text[0:23]) or
                (n == 0) or ("Posse(em virtude de" in ocorrencia.text)) and ("Afastamento(em virtude de" not in ocorrencia.text):
            entra = ocorrencia.text
            entra = entra.split(" ")[0]
            countE += 1
        else:
            sai = ocorrencia.text
            sai = sai.split(" ")[0]
            countS += 1
            if countE == countS:
                periodo = entra + " até " + sai
                atuacao.append(periodo)

    if entra not in str(atuacao):
        periodo = entra + " ..."
        atuacao.append(periodo)

    exercicio = str(atuacao).replace("[", "")
    exercicio = exercicio.replace("]", "")
    exercicio = exercicio.replace("'", "")
    lista.append([deputado, exercicio])
    print([deputado, exercicio])

    browser.back()
    time.sleep(1)


with open('Atuacao_Deputados.csv', 'w', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    for row in lista:
        print("Writing :", row)
        writer.writerows([row])

browser.close()
