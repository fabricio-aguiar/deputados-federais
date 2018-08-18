from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from unicodedata import normalize
from string import punctuation
import pandas as pd
import csv


def remover_acentos(txt):
    txt = ''.join([letter for letter in txt if letter not in punctuation])
    txt = txt.upper()
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')


print("\nBens Deputados")

options = Options()
options.add_argument("--start-maximized")


browser = webdriver.Chrome(chrome_options=options)

lista = [[
    'Nome',
    'Nome para Urna',
    'Numero',
    'Partido',
    'Coligação',
    'Situação',
    'Votação',
    '% Validos',
    'Sexo',
    'Estado Civil',
    'Ocupacao',
    'Cor/Raca',
    'Data Nasc.',
    'Idade',
    'Instrucao',
    'Bens',
    'UF',
    'foto'
]]

df = pd.read_csv('Detalhes_Deputados.csv', encoding='utf-8')
df = df[df['Legislatura'] == 55]
df['Nome'] = df['Nome'].apply(lambda x: remover_acentos(x))

dados = pd.read_csv('Resultado_da_Eleicao.csv', encoding='latin1', sep=';')
dados['Candidato'] = dados['Candidato'].apply(lambda x: remover_acentos(str(x)))
dados['UF'].fillna(value='-', inplace=True)
for i, row in enumerate(dados['UF']):
    if row != "-":
        aux = row
    else:
        dados.set_value(index=i, col='UF', value=aux)

for uf in df['UF'].unique():
    browser.get("http://inter01.tse.jus.br/divulga-cand-2014/eleicao/2014/UF/" + uf + "/candidatos/cargo/6")
    browser.set_page_load_timeout(20)
    estados = df[df['UF'] == uf]
    filtroUF = dados[dados['UF'] == uf]
    provisorio = []
    for i, deputado in enumerate(estados['Nome']):
        numero = dados[dados['Candidato'] == deputado]['Nr'].unique()
        partido = dados[dados['Candidato'] == deputado]['Partido'].unique()
        if len(numero) == 0:
            numero = deputado
            partido = 'Deferido'
        else:
            numero = str(numero[0]).replace(".0", "")
            partido = partido[0]
        if partido == 'PR':
            partido = numero
        # print("Numero: " + numero)
        browser.find_element_by_xpath("//*[@id='tbl-candidatos_filter']/label/input").send_keys(numero)
        try:
            browser.find_element_by_xpath('//*[contains(text(), "' + partido + '")]').click()

        except:
            browser.find_element_by_xpath("//*[@id='tbl-candidatos_filter']/label/input").clear()
            nom = estados.iloc[i]['Nome Parlamentar']
            provisorio.append(nom)
            if nom != remover_acentos(nom):
                provisorio.append(remover_acentos(nom))
            for parlamentar in provisorio:
                print(parlamentar)
                for char in parlamentar:
                    browser.find_element_by_xpath("//*[@id='tbl-candidatos_filter']/label/input").send_keys(char)
                    if len(browser.find_elements_by_xpath('//*[contains(text(), "Deferido")]')) == 1:
                        break
                try:
                    browser.find_element_by_xpath('//*[contains(text(), "Deferido")]').click()
                    provisorio[:] = []

                except:
                    browser.find_element_by_xpath("//*[@id='tbl-candidatos_filter']/label/input").clear()
                    continue
        while True:
            try:
                nome = browser.find_element_by_xpath("/html/body/div/div[4]/table/tbody/tr[2]/td[1]").text
                break
            except:
                pass
        nome = deputado
        nomeUrna = browser.find_element_by_xpath("/html/body/div/div[4]/table/tbody/tr[1]/td[1]").text
        numero = browser.find_element_by_xpath("/html/body/div/div[4]/table/tbody/tr[1]/td[2]").text
        res = filtroUF[filtroUF['Nr'] == float(numero)]
        partido = res['Partido'].unique()[0]
        coligacao = res['Coligação'].unique()[0]
        situacao = res['Situação'].unique()[0]
        voto = res['Votação'].unique()[0]
        validos = res['% Válidos'].unique()[0]
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
        linha = [
            nome,
            nomeUrna,
            numero,
            partido,
            coligacao,
            situacao,
            voto,
            validos,
            sexo,
            estCivil,
            ocupacao,
            cor,
            data,
            idade,
            instrucao,
            bem.replace(".", ""),
            uf,
            foto
        ]
        if linha not in lista:
            lista.append(linha)
        print(linha)
        browser.back()


with open('Bens_Deputados.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for row in lista:
        print("Writing :", row)
        writer.writerows([row])

browser.close()
