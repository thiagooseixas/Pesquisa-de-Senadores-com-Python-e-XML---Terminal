# -*- coding: utf-8 -*-
"""

O Senado Federal disponibiliza diversas APIs REST de dados abertos para o publico,
sendo que um dos endpoints descreve os Senadores em exercicio atualmente.
Dado este endpoint (http://legis.senado.gov.br/dadosabertos/senador/lista/atual),
crie um modelo de dados (ORM ou classes OO) que permita facil acesso e manuseio a Senadores em atividade e seus
 respectivos mandatos.

"""

import urllib2
import xml.etree.ElementTree as ET
import os
import sys

def pesquisaParlamentar(opcao):

    url = 'http://legis.senado.gov.br/dadosabertos/senador/lista/atual'
    codigo = ''

    if(opcao == 2):
        dadosParlamentar = raw_input("Por Nome, Partido ou Região: ")

        #tratando nomes quando pesquisada com minusculo ou minusculo
        dadosParlamentar = dadosParlamentar[0].upper() + dadosParlamentar[1:].lower()
        #tratando siglas do partido quando pesquisada
        if (len(dadosParlamentar) == 2) or (len(dadosParlamentar) == 3):
            dadosParlamentar = dadosParlamentar.upper()

    try:
        file = urllib2.urlopen(url)
        tree = ET.parse(file).getroot()
    except Exception as error:
        print 'Erro ao conectar a base de dados.', error
        sys.exit(1)

    for lis in tree.findall('Metadados'):
        print "\n-----* RESULTADO *-----\n"
        print 'Pesquisado em: ', lis.find('Versao').text

    for lista in tree.findall('Parlamentares'):
        for parlamentar in lista:

            for mandato in parlamentar.findall('Mandato'):
                codigo = mandato.find('CodigoMandato').text

            for identificacao in parlamentar.findall('IdentificacaoParlamentar'):

                nomeParlamentar = identificacao.find('NomeParlamentar').text
                partido = identificacao.find('SiglaPartidoParlamentar').text
                estado = identificacao.find('UfParlamentar').text

                if (opcao == 1):
                    print 'Senador(a): ', nomeParlamentar, '. ', partido, '-', estado

                elif (opcao == 2):
                    for nome in nomeParlamentar.split(" "):
                        if (dadosParlamentar == nome) or (dadosParlamentar == nome)\
                                or (dadosParlamentar == partido) or (dadosParlamentar == estado):
                            print 'Senador(a): ', nomeParlamentar, '. ', partido, '-', estado#, 'Mandato: ', codigo
                else:
                    print "Nao encontrado"


def inputPesquisa():
    print "-----* DADOS PARLAMENTARES *-----\n"
    pesquisar = input("1 - Ver Todos:\n2 - Pesquisar: ")

    if  pesquisar:
        pesquisaParlamentar(pesquisar)
    else:
        print 'ERRO'
        #os.system('clear')
        inputPesquisa()

inputPesquisa()