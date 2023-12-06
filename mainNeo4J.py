from neo4j import GraphDatabase
from utilities import *
from tabulate import tabulate

uri = "bolt://localhost:7687"  # Update with your Neo4j server URI
username = "neo4j"
password = "123"

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
        2: "MATCH (f:Funcionario) RETURN f ORDER BY f.idFuncionario ASC",
        3: "MATCH (ca:Cargo) RETURN ca ORDER BY ca.idCargo ASC",
        4: "MATCH (v:Venda) RETURN v ORDER BY v.idVendas ASC",
        5: "MATCH (e:Evento) RETURN e ORDER BY e.idEvento ASC",
        6: "MATCH (te:TipoEvento) RETURN te ORDER BY te.idTipoEvento ASC",
        7: "MATCH (i:Ingresso) RETURN i ORDER BY i.idIngresso ASC",
    }

    with connection._driver.session() as session:
        if opcaoTabela in queries:
            result = session.run(queries[opcaoTabela])
            resultado = [record[0] for record in result]
            headers = ["ID Cliente", "Nome", "Email", "Telefone"] if opcaoTabela == 1 else \
                      ["ID Funcionário", "Nome", "Email", "ID Cargo"] if opcaoTabela == 2 else \
                      ["ID Cargo", "Descrição"] if opcaoTabela == 3 else \
                      ["ID Vendas", "ID Cliente", "ID Funcionario", "Data Compra"] if opcaoTabela == 4 else \
                      ["ID Evento", "Local", "Maximo Ingressos", "Data", "Tipo Evento"] if opcaoTabela == 5 else \
                      ["ID Tipo Evento", "Descrição"] if opcaoTabela == 6 else \
                      ["ID Ingresso", "ID Evento", "ID Vento", "Valor Ingresso", "Quantidade"]
            print(tabulate(resultado, headers=headers))

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

        # ... (remaining code)

        #Cadastro
        elif opcaoMenu == 1:
            opcaoTabela = showTabelas()

            inserts = {
                1: ("Cliente", "nome", "email", "telefone"),
                2: ("Funcionario", "nome", "email"),
                3: ("Cargo", "descricao"),
                4: ("Venda", "idcliente", "idfuncionario", "dtcompra"),
                5: ("Evento", "local", "maxingressos", "data", "idtipo"),
                6: ("TipoEvento", "descricao"),
                7: ("Ingresso", "idevento", "idvenda", "valoringresso", "quantidade"),
            }

            if opcaoTabela in inserts:
                table_name, *properties = inserts[opcaoTabela]
                values = solicita_informacoes(table_name, *properties)
                properties_str = ', '.join(properties)
                query = f"CREATE ({table_name.lower()}:{table_name} {{{properties_str}: $values}})"
                neo4j_conn.execute(query, values=values)

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
                values = solicita_informacoes(table_name, "chave")
                query = f"MATCH ({table_name.lower()}:{table_name} {{id{table_name}: $values.chave}}) DETACH DELETE {table_name.lower()}"
                neo4j_conn.execute(query, values=values)

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