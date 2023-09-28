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

def showConsultas(opcaoTabela):

        if opcaoTabela == 1:#Cliente
            
            cursor.execute("SELECT * from clientes ORDER BY 1 ASC")
            resultado = cursor.fetchall()
            print(tabulate(resultado, ["ID Cliente", "Nome", "Email", "Telefone"]))

        elif opcaoTabela == 2:#Funcionarios
            
            cursor.execute("SELECT * from funcionarios ORDER BY 1 ASC")
            resultado = cursor.fetchall()
            print(tabulate(resultado, ["ID Funcionário","Nome","Email","ID Cargo"]))

        elif opcaoTabela == 3:#Cargo

            cursor.execute("SELECT * from cargos ORDER BY 1 ASC")
            resultado = cursor.fetchall()
            print(tabulate(resultado, ["ID Cargo","Descrição"]))

        elif opcaoTabela == 4:#Venda

            cursor.execute("SELECT * from vendas ORDER BY 1 ASC")
            resultado = cursor.fetchall()
            print(tabulate(resultado, ["ID Vendas", "ID Cliente", "ID Funcionario", "Data Compra"]))

        elif opcaoTabela == 5:#Evento

            cursor.execute("SELECT * from eventos ORDER BY 1 ASC")
            resultado = cursor.fetchall()
            print(tabulate(resultado, ["ID Evento", "Local", "Maximo Ingressos", "Data", "Tipo Evento"]))

        elif opcaoTabela == 6:#TipoEvento

            cursor.execute("SELECT * from tipoeventos ORDER BY 1 ASC")
            resultado = cursor.fetchall()
            print(tabulate(resultado, ["ID Tipo Evento", "Descrição"]))

        elif opcaoTabela == 7:#Ingresso

            cursor.execute("SELECT * from ingressos ORDER BY 1 ASC")
            resultado = cursor.fetchall()
            print(tabulate(resultado, ["ID Ingresso", "ID Evento", "ID Vento", "Valor Ingresso", "Quantidade"]))

        input("\nAperte qualquer tecla para continuar")

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

            #Mostra Cargos
            cursor.execute("SELECT * from cargos ORDER BY 1 ASC")
            resultado = cursor.fetchall()
            print(tabulate(resultado, ["ID Cargo","Descrição"]))

            idcargo = solicita_informacoes("Tipo Cargo", "chave")
            cursor.execute("INSERT INTO funcionarios (nome, email, idcargo) VALUES (%s,%s,%s);", (nome, email, idcargo))

        elif opcaoTabela == 3:#Cargo
            descricao = solicita_informacoes("Cargo", "descricao")
            cursor.execute(f"INSERT INTO cargos (descricao) VALUES ('{descricao}');")

        elif opcaoTabela == 4:#Venda

            #Mostra Clientes
            cursor.execute("SELECT * from clientes ORDER BY 1 ASC")
            resultado = cursor.fetchall()
            print(tabulate(resultado, ["ID Cliente", "Nome", "Email", "Telefone"]))

            idCliente = solicita_informacoes("Cliente", "chave")

            #Mostra Funcionarios
            cursor.execute("SELECT * from funcionarios ORDER BY 1 ASC")
            resultado = cursor.fetchall()
            print(tabulate(resultado, ["ID Funcionário","Nome","Email","ID Cargo"]))

            idFuncionario = solicita_informacoes("Funcionario", "chave")
            dtCompra = solicita_informacoes("Venda", "data_compra")            

            cursor.execute("SELECT idevento, local, data FROM eventos ORDER BY 1 ASC;")
            resultado = cursor.fetchall()

            print(tabulate(resultado, ["ID Evento", "Local", "Data"]))

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

            #Mostra Tipo Evento
            cursor.execute("SELECT * from tipoeventos ORDER BY 1 ASC")
            resultado = cursor.fetchall()
            print(tabulate(resultado, ["ID Tipo Evento", "Descrição"]))

            idTipo = solicita_informacoes("Tipo Evento", "chave")
            cursor.execute("INSERT INTO eventos (local, maxingressos, data, idtipo) VALUES (%s,%s,%s,%s);",(local, maxingressos, dtEvento, idTipo))
        
        elif opcaoTabela == 6:#TipoEvento
            descricao = solicita_informacoes("Tipo Evento", "descricao")
            cursor.execute(f"INSERT INTO tipoeventos (descricao) VALUES ('{descricao}');")

    #Atualização
    elif opcaoMenu == 2:
        opcaoTabela = showTabelas()

        if opcaoTabela == 1:#Cliente
            showConsultas(1)
            chave, nome, email, telefone = solicita_informacoes("Cliente", "chave", "nome", "email", "telefone")
            cursor.execute("UPDATE clientes SET nome = %s, email = %s, telefone = %s WHERE idcliente = %s;", (nome, email, telefone, chave))

        elif opcaoTabela == 2:#Funcionarios
            showConsultas(2)
            chave, nome, email = solicita_informacoes("Funcionario","chave","nome","email")
            idcargo = solicita_informacoes("Tipo Cargo", "chave")
            cursor.execute("UPDATE funcionarios SET nome = %s, email = %s, idcargo = %s WHERE idfuncionario = %s;", (nome, email, idcargo, chave))

        elif opcaoTabela == 3:#Cargo
            showConsultas(3)
            chave, descricao = solicita_informacoes("Cargo", "chave","descricao")
            cursor.execute("UPDATE cargos SET descricao = %s WHERE idcargo = %s;", (descricao, chave))

        elif opcaoTabela == 4:#Venda
            showConsultas(4)
            idCliente = solicita_informacoes("Cliente", "chave")
            idFuncionario = solicita_informacoes("Funcionario", "chave")
            chave, dtCompra = solicita_informacoes("Venda", "chave", "data_compra")
            cursor.execute("UPDATE vendas SET idcliente = %s, idfuncionario = %s, dtcompra = %s WHERE idvenda = %s;",(idCliente, idFuncionario, dtCompra, chave))
        
        elif opcaoTabela == 5:#Evento
            showConsultas(5)
            chave, local, maxingressos, dtEvento = solicita_informacoes("Evento","chave","local","maxingressos","data_evento")
            idTipo = solicita_informacoes("Tipo Evento", "chave")
            cursor.execute("UPDATE eventos SET local = %s, maxingressos = %s, data = %s, idtipo = %s WHERE idevento = %s ;",(local, maxingressos, dtEvento, idTipo, chave))
        
        elif opcaoTabela == 6:#TipoEvento
            showConsultas(6)
            chave, descricao = solicita_informacoes("Tipo Evento", "chave", "descricao")
            cursor.execute("UPDATE tipoeventos SET descricao = %s WHERE idtipoevento = %s;", (descricao, chave))
        
    #Remoção
    elif opcaoMenu == 3:
        opcaoTabela = showTabelas()

        if opcaoTabela == 1:#Cliente
            showConsultas(1)
            chave = solicita_informacoes("Cliente", "chave")
            cursor.execute(f"DELETE FROM clientes WHERE idcliente = {chave};")

        elif opcaoTabela == 2:#Funcionarios
            showConsultas(2)
            chave = solicita_informacoes("Funcionario","chave")
            cursor.execute(f"DELETE FROM funcionarios WHERE idfuncionario = {chave};")

        elif opcaoTabela == 3:#Cargo
            showConsultas(3)
            chave = solicita_informacoes("Cargo", "chave")
            cursor.execute(f"DELETE FROM cargos WHERE descricao = {chave};")

        elif opcaoTabela == 4:#Venda
            showConsultas(4)
            chave = solicita_informacoes("Venda", "chave")
            cursor.execute(f"DELETE FROM vendas WHERE idvenda = {chave};")
        
        elif opcaoTabela == 5:#Evento
            showConsultas(5)
            chave = solicita_informacoes("Evento","chave")
            cursor.execute(f"DELETE eventos WHERE idevento = {chave} ;")
        
        elif opcaoTabela == 6:#TipoEvento
            showConsultas(6)
            chave = solicita_informacoes("Tipo Evento", "chave")
            cursor.execute(f"DELETE tipoeventos WHERE idtipoevento = {chave};")
        
    #Consulta
    elif opcaoMenu == 4:
        opcaoTabela = showTabelas(True)

        showConsultas(opcaoTabela)
    

    #Relatórios    
    elif opcaoMenu == 5:
        opcaoRelatorio = showRelatorio()

        if opcaoRelatorio == 1:
            cursor.execute("SELECT e.idEvento, e.local AS local_do_evento, e.data AS data_do_evento, e.maxIngressos AS limite_de_ingressos, COUNT(v.idVenda) AS total_de_vendas, SUM(i.valorIngresso * i.quantidade) AS receita_total FROM eventos e LEFT JOIN ingressos i ON e.idEvento = i.idEvento LEFT JOIN vendas v ON i.idVenda = v.idVenda GROUP BY e.idEvento, e.local, e.data, e.maxIngressos ORDER BY data_do_evento ASC;")
            resultado = cursor.fetchall()
            print(tabulate(resultado, ["ID Evento", "Local", "Data do Evento", "Limite Ingressos", "Ingressos Vendidos", "Receita Total"]))

        elif opcaoRelatorio == 2:
            cursor.execute("SELECT f.idFuncionario, f.nome AS nome_do_funcionario, COUNT(v.idVenda) AS total_de_vendas, SUM(i.valorIngresso * i.quantidade) AS receita_total FROM funcionarios f LEFT JOIN vendas v ON f.idFuncionario = v.idFuncionario LEFT JOIN ingressos i ON v.idVenda = i.idVenda GROUP BY f.idFuncionario, f.nome ORDER BY nome_do_funcionario ASC;")
            resultado = cursor.fetchall()
            print(tabulate(resultado, ["ID Funcionário", "Nome Funcionário", "Total de Vendas", "Receita Total"]))

        elif opcaoRelatorio == 3:

            cursor.execute("SELECT te.descricao AS tipo_evento, COUNT(e.idEvento) AS quantidade_de_eventos FROM tipoeventos te LEFT JOIN eventos e ON te.idTipoEvento = e.idTipo GROUP BY te.descricao ORDER BY te.descricao ASC;")
            resultado = cursor.fetchall()
            print(tabulate(resultado, ["Tipo do Evento", "Quantidade de Eventos"]))
        
        input("\nAperte qualquer tecla para continuar")

    os.system("cls")






    
    
    

    


    

    
