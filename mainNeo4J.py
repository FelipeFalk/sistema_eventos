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
                    [record["ID_Venda"], record["ID_Cliente"], record["ID_Funcionario"], str(record["DT_Compra"])] if opcaoTabela == 4 else \
                    [record["ID_Evento"], record["Local"], record["Maximo_Ingressos"], str(record["Data"]), record["ID_Tipo"]] if opcaoTabela == 5 else \
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
                2: ("Funcionario", "idFuncionario","nome", "email", "idCargo"),
                3: ("Cargo", "idCargo","descricao"),
                4: ("Venda", "idVenda","idCliente", "idFuncionario", "dtcompra"),
                5: ("Evento", "idEvento","local", "maxingressos", "data", "idTipoEvento"),
                6: ("TipoEvento", "idTipoEvento","descricao"),
                7: ("Ingresso", "idIngresso","idEvento", "idVenda", "valoringresso", "quantidade"),
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
                    #table_name = "Cargo"
                    #chave_value = int(input(f"Digite o ID {table_name}"))
                    query = f"""MATCH (funcionario:Funcionario {{idFuncionario: '{values[0]}'}}), (cargo:Cargo {{idCargo: '{values[3]}'}})
                    CREATE (funcionario)-[:OCUPA]->(cargo)"""
                    neo4j_conn.execute(query)

                elif opcaoTabela == 4:
                    #table_name = "Cliente"
                    #chave_value = int(input(f"Digite o ID {table_name}"))
                    #table_name2 = "Funcionario"
                    #chave_value2 = int(input(f"Digite o ID {table_name}"))
                    query = f"""MATCH (venda:Venda {{idVenda: '{values[0]}'}}), (cliente:Cliente {{idCliente: '{values[1]}'}}), (funcionario:Funcionario {{idFuncionario: '{values[2]}'}})
                                        CREATE (venda)-[:REALIZADA_POR]->(funcionario),
                                               (venda)-[:PERTENCE_AO_CLIENTE]->(cliente)"""
                    neo4j_conn.execute(query)
                elif opcaoTabela == 5:
                    #table_name = "TipoEvento"
                    #chave_value = int(input(f"Digite o ID {table_name}"))
                    query = f"""MATCH (evento:Evento {{idEvento: '{values[0]}'}}), (tipoEvento:TipoEvento {{idTipoEvento: '{values[4]}'}})
                                        CREATE (evento)-[:PERTENCE_AO_TIPO]->(tipoEvento)"""
                    neo4j_conn.execute(query)
                elif opcaoTabela == 7:
                    #table_name = "Evento"
                    #chave_value = int(input(f"Digite o ID {table_name}"))
                    #table_name = "Venda"
                    #chave_value2 = int(input(f"Digite o ID {table_name}"))
                    query = f"""MATCH (ingresso:Ingresso {{idIngresso: '{values[0]}'}}), (evento:Evento {{idEvento: '{values[1]}'}}), (venda:Venda {{idVenda: '{values[2]}'}})
                                                            CREATE (ingresso)-[:PARA_EVENTO]->(evento),
                                                                   (ingresso)-[:VENDIDO_EM]->(venda)"""
                    neo4j_conn.execute(query)
        #Atualização
        elif opcaoMenu == 2:
            print("em construção")


        #Consulta
        elif opcaoMenu == 4:
            opcaoTabela = showTabelas(True)
            showConsultas(opcaoTabela, neo4j_conn)

        #Relatórios    
        elif opcaoMenu == 5:
            queries = {
                1: """MATCH (f:Funcionario)-[:OCUPA]->(c:Cargo)
                        RETURN f.idFuncionario AS ID_Funcionario, f.nome AS Nome, f.email AS Email, c.idCargo AS ID_Cargo
                        ORDER BY f.idFuncionario ASC""",
                2: """MATCH (v:Venda)-[:REALIZADA_POR]->(f:Funcionario), (v)-[:PERTENCE_AO_CLIENTE]->(c:Cliente)
                        RETURN v.idVenda AS ID_Venda, c.idCliente AS ID_Cliente, f.idFuncionario AS ID_Funcionario, v.dtCompra AS DT_Compra
                        ORDER BY v.idVenda ASC""",
                3: """MATCH (e:Evento)-[:PERTENCE_AO_TIPO]->(te:TipoEvento)
                        RETURN e.idEvento AS ID_Evento, e.local AS Local, e.maxIngressos AS Maximo_Ingressos, e.data AS Data, te.idTipoEvento AS ID_Tipo
                        ORDER BY e.idEvento ASC"""
            }

            with neo4j_conn._driver.session() as session:
                opcaoRelatorio = showRelatorio()
                if opcaoRelatorio in queries:
                    result = session.run(queries[opcaoRelatorio])
                    resultado = result if opcaoRelatorio in (2, 4, 5, 7) else result.values()

                    headers = (
                        ["ID Funcionário", "Nome", "Email", "ID Cargo"] if opcaoRelatorio == 1 else
                        ["ID Vendas", "ID Cliente", "ID Funcionario", "Data Compra"] if opcaoRelatorio == 2 else
                        ["ID Evento", "Local", "Maximo Ingressos", "Data",
                         "Tipo Evento"] if opcaoRelatorio == 3 else None
                    )

                    table = PrettyTable(headers)
                    for record in resultado:
                        if isinstance(record, dict):
                            row = [record["ID_Funcionario"], record["Nome"], record["Email"],
                                   record["ID_Cargo"]] if opcaoRelatorio == 1 else \
                                [record["ID_Venda"], record["ID_Cliente"], record["ID_Funcionario"],
                                 str(record["DT_Compra"])] if opcaoRelatorio == 2 else \
                                    [record["ID_Evento"], record["Local"], record["Maximo_Ingressos"],
                                     str(record["Data"]), record["ID_Tipo"]] if opcaoRelatorio == 3 else None

                            if row is not None:
                                table.add_row(row)

                    print(table)

            input("\nAperte qualquer tecla para continuar")
            os.system("cls")


finally:
    neo4j_conn.close()