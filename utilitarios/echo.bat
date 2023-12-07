@echo off

echo Creating clientes.csv...
echo idCliente,nome,email,telefone > clientes.csv
echo 1,Cliente 1,cliente1@example.com,(47)-91111-1111 >> clientes.csv
echo 2,Cliente 2,cliente2@example.com,(47)-91111-1112 >> clientes.csv
echo 3,Cliente 3,cliente3@example.com,(47)-91111-1113 >> clientes.csv
echo 4,Cliente 4,cliente4@example.com,(47)-91111-1114 >> clientes.csv
echo 5,Cliente 5,cliente5@example.com,(47)-91111-1115 >> clientes.csv

echo Creating tipoeventos.csv...
echo idTipoEvento,descricao > tipoeventos.csv
echo 1,Concerto >> tipoeventos.csv
echo 2,Conferência >> tipoeventos.csv
echo 3,Exposição >> tipoeventos.csv
echo 4,Teatro >> tipoeventos.csv
echo 5,Esporte >> tipoeventos.csv

echo Creating eventos.csv...
echo idEvento,local,maxIngressos,data,idTipo > eventos.csv
echo 1,Local 1,100,2023-10-15,1 >> eventos.csv
echo 2,Local 2,200,2023-11-20,2 >> eventos.csv
echo 3,Local 3,150,2023-12-05,3 >> eventos.csv
echo 4,Local 4,50,2023-10-30,4 >> eventos.csv
echo 5,Local 5,300,2023-12-15,5 >> eventos.csv

echo Creating cargos.csv...
echo idCargo,descricao > cargos.csv
echo 1,Gerente >> cargos.csv
echo 2,Vendedor >> cargos.csv
echo 3,Atendente >> cargos.csv
echo 4,Técnico >> cargos.csv
echo 5,Analista >> cargos.csv

echo Creating funcionarios.csv...
echo idFuncionario,nome,email,idCargo > funcionarios.csv
echo 1,Funcionário 1,funcionario1@example.com,1 >> funcionarios.csv
echo 2,Funcionário 2,funcionario2@example.com,2 >> funcionarios.csv
echo 3,Funcionário 3,funcionario3@example.com,2 >> funcionarios.csv
echo 4,Funcionário 4,funcionario4@example.com,3 >> funcionarios.csv
echo 5,Funcionário 5,funcionario5@example.com,4 >> funcionarios.csv

echo Creating vendas.csv...
echo idVenda,idCliente,idFuncionario,dtCompra > vendas.csv
echo 1,1,1,2023-10-16 >> vendas.csv
echo 2,2,2,2023-11-21 >> vendas.csv
echo 3,3,3,2023-12-06 >> vendas.csv
echo 4,4,4,2023-10-31 >> vendas.csv
echo 5,5,5,2023-12-16 >> vendas.csv

echo Creating ingressos.csv...
echo idIngresso,idEvento,idVenda,valorIngresso,quantidade > ingressos.csv
echo 1,1,1,50.00,2 >> ingressos.csv
echo 2,2,2,30.00,3 >> ingressos.csv
echo 3,3,3,25.00,5 >> ingressos.csv
echo 4,4,4,40.00,1 >> ingressos.csv
echo 5,5,5,20.00,4 >> ingressos.csv

echo CSV files created successfully!
