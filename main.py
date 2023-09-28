from utilities import *
import psycopg2
from tabulate import tabulate
from datetime import datetime
import os

dbname='db_eventos'
user='postgres'
password='123'

conn = psycopg2.connect(f"dbname={dbname} user={user} password={password}")
cursor = conn.cursor()
conn.autocommit = True

cond = True

while cond == True:
    opcaoMenu = showMenu()

    if opcaoMenu == 0:
        cursor.close()
        conn.close()
        cond = False

    #Cadastro
    if opcaoMenu == 1:
        opcaoTabela = showTabelas()

        if opcaoTabela == 1:#Cliente
            nome, email, telefone = solicita_informacoes("Cliente", "nome", "email", "telefone")
            cursor.execute("INSERT INTO clientes (nome, email, telefone) VALUES (%s, %s, %s);", (nome, email, telefone))

        elif opcaoTabela == 2:#Funcionarios
            nome, email = solicita_informacoes("Funcionario","nome","email")
            idcargo = solicita_informacoes("Tipo Cargo", "chave")
            cursor.execute("INSERT INTO funcionarios (nome, email, idcargo) VALUES (%s,%s,%s);", (nome, email, idcargo))

        elif opcaoTabela == 3:#Cargo
            descricao = solicita_informacoes("Cargo", "descricao")
            cursor.execute(f"INSERT INTO cargos (descricao) VALUES ('{descricao}');")

        elif opcaoTabela == 4:#Venda
            idCliente = solicita_informacoes("Cliente", "chave")
            idFuncionario = solicita_informacoes("Funcionario", "chave")
            dtCompra = solicita_informacoes("Venda", "data_compra")            

            headers = ["ID Evento", "Local", "Data"]

            cursor.execute("SELECT idevento, local, data FROM eventos;")
            resultado = cursor.fetchall()

            print(tabulate(resultado, headers))

            chaveEvento = solicita_informacoes("Evento", "chave")

            preco = float(input("Digite o preço do ingresso:\n"))

            cursor.execute(f"SELECT e.maxIngressos, COUNT(i.idIngresso) AS ingressos_vendidos FROM eventos e LEFT JOIN ingressos i ON e.idEvento = i.idEvento WHERE e.idEvento = {chaveEvento} GROUP BY e.idEvento, e.maxIngressos")
            resultado = cursor.fetchone()

            if resultado[0] > resultado[1]:
                cursor.execute("INSERT INTO vendas (idcliente, idfuncionario, dtcompra) VALUES (%s,%s,%s) RETURNING idvenda;",(idCliente, idFuncionario, dtCompra))
                idvenda = cursor.fetchone()[0]
                cursor.execute("INSERT INTO ingressos (idevento, idvenda, valoringresso, quantidade) VALUES (%s,%s,%s,%s);",(chaveEvento, idvenda, preco, 1))

            else:
                print("Quantidade máxima de ingressos vendidos")
            
        
        elif opcaoTabela == 5:#Evento
            local, maxingressos, dtEvento = solicita_informacoes("Evento","local","maxingressos","data_evento")
            idTipo = solicita_informacoes("Tipo Evento", "chave")
            cursor.execute("INSERT INTO eventos (local, maxingressos, data, idtipo) VALUES (%s,%s,%s,%s);",(local, maxingressos, dtEvento, idTipo))
        
        elif opcaoTabela == 6:#TipoEvento
            descricao = solicita_informacoes("Tipo Evento", "descricao")
            cursor.execute(f"INSERT INTO tipoeventos (descricao) VALUES ('{descricao}');")

    #Atualização
    elif opcaoMenu == 2:
        opcaoTabela = showTabelas()

        if opcaoTabela == 1:#Cliente
            chave, nome, email, telefone = solicita_informacoes("Cliente", "chave", "nome", "email", "telefone")
            cursor.execute("UPDATE clientes SET nome = %s, email = %s, telefone = %s WHERE idcliente = %s;", (nome, email, telefone, chave))

        elif opcaoTabela == 2:#Funcionarios
            chave, nome, email = solicita_informacoes("Funcionario","chave","nome","email")
            idcargo = solicita_informacoes("Tipo Cargo", "chave")
            cursor.execute("UPDATE funcionarios SET nome = %s, email = %s, idcargo = %s WHERE idfuncionario = %s;", (nome, email, idcargo, chave))

        elif opcaoTabela == 3:#Cargo
            chave, descricao = solicita_informacoes("Cargo", "chave","descricao")
            cursor.execute("UPDATE cargos SET descricao = %s WHERE idcargo = %s;", (descricao, chave))

        elif opcaoTabela == 4:#Venda
            idCliente = solicita_informacoes("Cliente", "chave")
            idFuncionario = solicita_informacoes("Funcionario", "chave")
            chave, dtCompra = solicita_informacoes("Venda", "chave", "data_compra")
            cursor.execute("UPDATE vendas SET idcliente = %s, idfuncionario = %s, dtcompra = %s WHERE idvenda = %s;",(idCliente, idFuncionario, dtCompra, chave))
        
        elif opcaoTabela == 5:#Evento
            chave, local, maxingressos, dtEvento = solicita_informacoes("Evento","chave","local","maxingressos","data_evento")
            idTipo = solicita_informacoes("Tipo Evento", "chave")
            cursor.execute("UPDATE eventos SET local = %s, maxingressos = %s, data = %s, idtipo = %s WHERE idevento = %s ;",(local, maxingressos, dtEvento, idTipo, chave))
        
        elif opcaoTabela == 6:#TipoEvento
            chave, descricao = solicita_informacoes("Tipo Evento", "chave", "descricao")
            cursor.execute("UPDATE tipoeventos SET descricao = %s WHERE idtipoevento = %s;", (descricao, chave))
        
    #Remoção
    elif opcaoMenu == 3:
        opcaoTabela = showTabelas()

        if opcaoTabela == 1:#Cliente
            chave = solicita_informacoes("Cliente", "chave")
            cursor.execute(f"DELETE FROM clientes WHERE idcliente = {chave};")

        elif opcaoTabela == 2:#Funcionarios
            chave = solicita_informacoes("Funcionario","chave")
            cursor.execute(f"DELETE FROM funcionarios WHERE idfuncionario = {chave};")

        elif opcaoTabela == 3:#Cargo
            chave = solicita_informacoes("Cargo", "chave")
            cursor.execute(f"DELETE FROM cargos WHERE descricao = {chave};")

        elif opcaoTabela == 4:#Venda
            chave = solicita_informacoes("Venda", "chave")
            cursor.execute(f"DELETE FROM vendas WHERE idvenda = {chave};")
        
        elif opcaoTabela == 5:#Evento
            chave = solicita_informacoes("Evento","chave")
            cursor.execute(f"DELETE eventos WHERE idevento = {chave} ;")
        
        elif opcaoTabela == 6:#TipoEvento
            chave = solicita_informacoes("Tipo Evento", "chave")
            cursor.execute(f"DELETE tipoeventos WHERE idtipoevento = {chave};")
        
    #Consulta
    elif opcaoMenu == 4:
        opcaoTabela = showTabelas()

        if opcaoTabela == 1:#Cliente
            
            cursor.execute("SELECT * from clientes")
            resultado = cursor.fetchall()
            print(tabulate(resultado, ["ID Cliente", "Nome", "Email", "Telefone"]))

        elif opcaoTabela == 2:#Funcionarios
            
            cursor.execute("SELECT * from funcionarios")
            resultado = cursor.fetchall()
            print(tabulate(resultado, ["ID Funcionário","Nome","Email","ID Cargo"]))

        elif opcaoTabela == 3:#Cargo

            cursor.execute("SELECT * from cargos")
            resultado = cursor.fetchall()
            print(tabulate(resultado, ["ID Cargo","Descrição"]))

        elif opcaoTabela == 4:#Venda

            cursor.execute("SELECT * from vendas")
            resultado = cursor.fetchall()
            print(tabulate(resultado, ["ID Vendas", "ID Cliente", "ID Funcionario", "Data Compra"]))

        elif opcaoTabela == 5:#Evento

            cursor.execute("SELECT * from eventos")
            resultado = cursor.fetchall()
            print(tabulate(resultado, ["ID Evento", "Local", "Maximo Ingressos", "Data", "Tipo Evento"]))

        elif opcaoTabela == 6:#TipoEvento

            cursor.execute("SELECT * from tipoeventos")
            resultado = cursor.fetchall()
            print(tabulate(resultado, ["ID Tipo Evento", "Descrição"]))

    
    
    

    #Relatórios


    

    
