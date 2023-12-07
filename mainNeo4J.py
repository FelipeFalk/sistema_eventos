from neo4j import GraphDatabase
from utilities import *
from tabulate import tabulate
from prettytable import PrettyTable
import os

uri = "bolt://localhost:7687"  # Update with your Neo4j server URI
username = "neo4j"
password = "12345678"

class Neo4jConnection:
    def __init__(self, uri, user, pwd):
        self._uri = uri
        self._user = user
        self._password = pwd
        self._driver = None

    def connect(self):
        self._driver = GraphDatabase.driver(self._uri, auth=(self._user, self._password))

    def close(self):
        if self._driver is not None:
            self._driver.close()

    def execute(self, query, **parameters):
        with self._driver.session() as session:
            return session.run(query, **parameters)

def showConsultas(opcaoTabela, connection):
    queries = {
        1: "MATCH (c:Cliente) RETURN c ORDER BY c.idCliente ASC",
        2: """MATCH (f:Funcionario)-[:OCUPA]->(c:Cargo)
            RETURN f.idFuncionario AS ID_Funcionario, f.nome AS Nome, f.email AS Email, c.idCargo AS ID_Cargo
            ORDER BY f.idFuncionario ASC""",
        3: "MATCH (ca:Cargo) RETURN ca ORDER BY ca.idCargo ASC",
        4: """MATCH (v:Venda)-[:REALIZADA_POR]->(f:Funcionario), (v)-[:PERTENCE_AO_CLIENTE]->(c:Cliente)
            RETURN v.idVenda AS ID_Venda, c.idCliente AS ID_Cliente, f.idFuncionario AS ID_Funcionario, v.dtCompra AS DT_Compra
            ORDER BY v.idVenda ASC""",
        5: """MATCH (e:Evento)-[:PERTENCE_AO_TIPO]->(te:TipoEvento)
            RETURN e.idEvento AS ID_Evento, e.local AS Local, e.maxIngressos AS Maximo_Ingressos, e.data AS Data, te.idTipoEvento AS ID_Tipo
            ORDER BY e.idEvento ASC""",
        6: "MATCH (te:TipoEvento) RETURN te ORDER BY te.idTipoEvento ASC",
        7: """MATCH (i:Ingresso)-[:PARA_EVENTO]->(e:Evento) MATCH (i)-[:VENDIDO_EM]->(v:Venda)
            RETURN i.idIngresso AS ID_Ingresso, v.idVenda AS ID_Venda, e.idEvento AS ID_Evento, i.valorIngresso AS Valor_Ingresso, i.quantidade AS Quantidade
            ORDER BY i.idIngresso ASC""",
    }

    with connection._driver.session() as session:
        if opcaoTabela in queries:
            result = session.run(queries[opcaoTabela])
            if opcaoTabela in (2, 4, 5, 7):
                resultado = result
            else:
                resultado = [record[0] for record in result]
            headers = (
                ["ID Cliente", "Nome", "Email", "Telefone"] if opcaoTabela == 1 else \
                ["ID Funcionário", "Nome", "Email", "ID Cargo"] if opcaoTabela == 2 else \
                ["ID Cargo", "Descrição"] if opcaoTabela == 3 else \
                ["ID Vendas", "ID Cliente", "ID Funcionario", "Data Compra"] if opcaoTabela == 4 else \
                ["ID Evento", "Local", "Maximo Ingressos", "Data", "Tipo Evento"] if opcaoTabela == 5 else \
                ["ID Tipo Evento", "Descrição"] if opcaoTabela == 6 else \
                ["ID Ingresso", "ID Evento", "ID Venda", "Valor Ingresso", "Quantidade"]
            )
            table = PrettyTable(headers)
            for record in resultado:
                row = [record["idCliente"], record["nome"], record["email"], record["telefone"]] if opcaoTabela == 1 else \
                    [record["ID_Funcionario"], record["Nome"], record["Email"], record["ID_Cargo"]] if opcaoTabela == 2 else \
                    [record["idCargo"], record["descricao"]] if opcaoTabela == 3 else \
                    [record["ID_Venda"], record["ID_Cliente"], record["ID_Funcionario"], record["DT_Compra"].strftime("%Y-%m-%d %H:%M:%S")] if opcaoTabela == 4 else \
                    [record["ID_Evento"], record["Local"], record["Maximo_Ingressos"], record["Data"].strftime("%Y-%m-%d %H:%M:%S"), record["ID_Tipo"]] if opcaoTabela == 5 else \
                    [record["idTipoEvento"], record["descricao"]] if opcaoTabela == 6 else \
                    [record["ID_Ingresso"], record["ID_Evento"], record["ID_Venda"], record["Valor_Ingresso"], record["Quantidade"]] if opcaoTabela == 7 else None

                if row is not None:
                    table.add_row(row)

            print(table)
                
    input("\nAperte qualquer tecla para continuar")

# Usage
try:
    neo4j_conn = Neo4jConnection(uri, username, password)
    neo4j_conn.connect()

    cond = True
    while cond:
        opcaoMenu = showMenu()

        if opcaoMenu == 0:
            cond = False

        #Cadastro
        elif opcaoMenu == 1:
            opcaoTabela = showTabelas()

            inserts = {
                1: ("Cliente", "idCliente", "nome", "email", "telefone"),
                2: ("Funcionario", "idFuncionario","nome", "email"),
                3: ("Cargo", "idCargo","descricao"),
                4: ("Venda", "idVenda","idcliente", "idfuncionario", "dtcompra"),
                5: ("Evento", "idEvento","local", "maxingressos", "data", "idtipo"),
                6: ("TipoEvento", "idTipoEvento","descricao"),
                7: ("Ingresso", "idIngresso","idevento", "idvenda", "valoringresso", "quantidade"),
            }

            if opcaoTabela in inserts:
                table_name, *properties = inserts[opcaoTabela]
                values = solicita_informacoes(table_name, *properties)

                #max_id_query = f"MATCH ({table_name.lower()}:{table_name}) RETURN max({table_name.lower()}.id{table_name}) AS max_id LIMIT 1"
                #result = neo4j_conn.execute(max_id_query)

                #Não estou conseguindo usar o Maior Id

                properties_str = ', '.join(properties)
                values_str = ','.join(f"'{valor}'" for valor in values)

                pairs = [f"{properties[i]}: '{values[i]}'" for i in range(len(properties))]
                pairs_str = ', '.join(pairs)

                query = f"CREATE ({table_name.lower()}:{table_name} {{{pairs_str}}})"
                neo4j_conn.execute(query)

                if opcaoTabela == 2: #Conecta Funcionario com Cargos
                    table_name = "Cargo"
                    chave_value = int(input(f"Digite o ID {table_name}"))
                    id_property = f"id{table_name}"
                    query = f"""MATCH (funcionario:Funcionario {{idFuncionario: toInteger({values[0]})}}), (cargo:Cargo {{idCargo: toInteger({chave_value})}})
                    CREATE (funcionario)-[:OCUPA]->(cargo)"""
                    neo4j_conn.execute(query)

                elif opcaoTabela == 4:
                    table_name = "Cliente"
                    chave_value = int(input(f"Digite o ID {table_name}"))
                    table_name = "Funcionario"
                    chave_value2 = int(input(f"Digite o ID {table_name}"))
                elif opcaoTabela == 5:
                    table_name = "TipoEvento"
                    chave_value = int(input(f"Digite o ID {table_name}"))
                elif opcaoTabela == 7:
                    table_name = "Evento"
                    chave_value = int(input(f"Digite o ID {table_name}"))
                    table_name = "Venda"
                    chave_value2 = int(input(f"Digite o ID {table_name}"))

        #Atualização
        elif opcaoMenu == 2:
            opcaoTabela = showTabelas()

            updates = {
                1: ("Cliente", "nome", "email", "telefone"),
                2: ("Funcionario", "nome", "email"),
                3: ("Cargo", "descricao"),
                4: ("Venda", "idcliente", "idfuncionario", "dtcompra"),
                5: ("Evento", "local", "maxingressos", "data", "idtipo"),
                6: ("TipoEvento", "descricao"),
                7: ("Ingresso", "idevento", "idvenda", "valoringresso", "quantidade"),
            }

            if opcaoTabela in updates:
                table_name, *properties = updates[opcaoTabela]
                showConsultas(opcaoTabela, neo4j_conn)
                values = solicita_informacoes(table_name, *["chave"] + properties)
                properties_str = ', '.join([f"{prop} = $values.{prop}" for prop in properties])
                query = f"MATCH ({table_name.lower()}:{table_name} {{id{table_name}: $values.chave}}) SET {properties_str}"
                neo4j_conn.execute(query, values=values)

        #Remoção
        elif opcaoMenu == 3:
            opcaoTabela = showTabelas()

            deletions = {
                1: "Cliente",
                2: "Funcionario",
                3: "Cargo",
                4: "Venda",
                5: "Evento",
                6: "TipoEvento",
                7: "Ingresso",
            }

            if opcaoTabela in deletions:
                table_name = deletions[opcaoTabela]
                showConsultas(opcaoTabela, neo4j_conn)

                id_property = f"id{table_name}"
                chave_value = int(input(f"Digite o ID {table_name}"))
                query = f"MATCH ({table_name.lower()}:{table_name} {{{id_property}: {chave_value}}}) DETACH DELETE {table_name.lower()}"

                neo4j_conn.execute(query)


        #Consulta
        elif opcaoMenu == 4:
            opcaoTabela = showTabelas(True)
            showConsultas(opcaoTabela, neo4j_conn)

        #Relatórios    
        elif opcaoMenu == 5:
            opcaoRelatorio = showRelatorio()

            reports = {
                1: "MATCH (e:Evento) RETURN e",
                # Add more cases for other reports...
            }

            if opcaoRelatorio in reports:
                query = reports[opcaoRelatorio]
                result = neo4j_conn.execute(query)
                resultado = [record[0] for record in result]
                print(tabulate(resultado, headers=["ID Evento", "Local", "Data do Evento", "Limite Ingressos", "Ingressos Vendidos", "Receita Total"]))

        os.system("cls")

finally:
    neo4j_conn.close()