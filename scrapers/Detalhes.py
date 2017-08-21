import pandas as pd
import numpy as np
import congresso as cn
from bs4 import BeautifulSoup 
import csv


dataset2017 = pd.read_csv('../Deputados/data/Ano-2017.csv', sep=';',
                         dtype={'idecadastro': np.str})
                                
dataset2016 = pd.read_csv('../Deputados/data/Ano-2016.csv', sep=';',
                         dtype={'idecadastro': np.str})
                                
dataset2015 = pd.read_csv('../Deputados/data/Ano-2015.csv', sep=';',
                         dtype={'idecadastro': np.str})



dataset = pd.concat([dataset2017, dataset2016, dataset2015])
codigos = dataset['idecadastro'].unique()

camara = cn.Camara()
lista = [['idecadastro', 'Legislatura', 'Nome', 'Nome Parlamentar', 'Profissao', 'Situacao na Legislatura Atual', 'Sexo', 'UF', 'Partido']]


for id in codigos:
    try:
        detalhes = camara.deputados.obter_detalhes_deputado(ideCadastro=int(id))
    except:
        continue
    bsoup = BeautifulSoup(detalhes['content'], "lxml")
    leg = bsoup.find('numlegislatura').text
    profissao = bsoup.find('nomeprofissao').text
    situacaoNaLegislaturaAtual = bsoup.find('situacaonalegislaturaatual').text
    nome = bsoup.find('nomecivil').text
    nomeparlamentar = bsoup.find('nomeparlamentaratual').text
    sexo = bsoup.find('sexo').text
    uf = bsoup.find('ufrepresentacaoatual').text
    partido = bsoup.find('sigla').text
    lista.append([id, leg, nome, nomeparlamentar, profissao.replace("\n","-"), situacaoNaLegislaturaAtual, sexo, uf, partido])
 
with open ('Detalhes_Deputados.csv','w', newline='') as file:
    writer=csv.writer(file)
    for row in lista:
        print("Writing :",row)
        writer.writerows([row])