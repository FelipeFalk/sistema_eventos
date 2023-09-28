import psycopg2
import os
from utilities import *
from tabulate import tabulate

def showMenu():
    #os.system("cls")
    print("Menu - Opções")
    print("1 - Cadastro")
    print("2 - Atualização")
    print("3 - Remoção")
    print("4 - Consulta")
    print("5 - Relatórios")
    print("0 - Sair")

    op = int(input("Informe a opção desejada\n"))

    return op

def showTabelas(Ingresso = False):
    #os.system("cls")
    print("Tabelas - Opções")
    print("1 - Cliente")
    print("2 - Funcionário")
    print("3 - Cargo")
    print("4 - Venda")
    print("5 - Evento")
    print("6 - Tipo Evento")

    if(Ingresso == True):
        print("7 - Ingressos")

    print("0 - Sair")

    op = int(input("Informe a tabela desejada\n"))

    return op

def solicita_informacoes(tipo, *infos):
    #os.system("cls")
    lista_informacoes = []
    for _infos in infos:
        entrada = None

        if _infos == "chave":
            entrada = input(f"Informe o ID do {tipo}:")

        elif _infos == "nome":
            entrada = input(f"Informe o nome completo do {tipo}:")
        
        elif _infos == "email":
            entrada = input(f'Informe o e-mail do {tipo}: ')

        elif _infos == "telefone":
            entrada = input(f'Informe o telefone do {tipo}: ')

        elif _infos == "descricao":
            entrada = input(f'Informe a descrição do {tipo}: ')

        elif _infos == "data_compra":
            entrada = input(f'Informe a data de compra da {tipo} (yyyy-mm-dd):')

        elif _infos == "local":
            entrada = input(f'Informe o local do {tipo}:')

        elif _infos == "maxingressos":
            entrada = int(input(f'Informe a quantidade máxima de ingressos do {tipo}:'))

        elif _infos == "data_evento":
            entrada = input(f'Informe a data do {tipo} (yyyy-mm-dd):')

        lista_informacoes.append(entrada)
        
    if len(lista_informacoes) == 1:
        return lista_informacoes[0]
    return lista_informacoes

def showRelatorio():

    #os.system("cls")
    print("Relatórios - Opções")
    print("1 - Relatório de Vendas por Eventos")
    print("2 - Relatório de Vendas por Funcionário")
    print("3 - Relatório de Quantidade de Eventos por Tipo")
    print("0 - Sair")

    op = int(input("Informe a tabela desejada\n"))
    return op