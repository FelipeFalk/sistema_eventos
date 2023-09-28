CREATE TABLE IF NOT EXISTS clientes
(
    idCliente SERIAL,
    nome VARCHAR(60),
    email VARCHAR(100) UNIQUE,
    telefone VARCHAR(15) NOT NULL,
    PRIMARY KEY (idCliente)
);


CREATE TABLE IF NOT EXISTS tipoeventos
(
    idTipoEvento SERIAL,
    descricao VARCHAR(255),
    PRIMARY KEY (idTipoEvento)
);

CREATE TABLE IF NOT EXISTS eventos
(
    idEvento SERIAL,
    local VARCHAR(255),
    maxIngressos integer,
    data date,
    idTipo integer NOT NULL,
    PRIMARY KEY (idEvento),
    CONSTRAINT fk_eventos_tipoevento FOREIGN KEY (idTipo) REFERENCES tipoeventos (idTipoEvento) ON DELETE CASCADE 
);

CREATE TABLE IF NOT EXISTS cargos
(
    idCargo SERIAL,
	descricao VARCHAR(255),
	PRIMARY KEY (idCargo)
);

CREATE TABLE IF NOT EXISTS funcionarios
(
    idFuncionario SERIAL,
    nome VARCHAR(60),
    email VARCHAR(100) UNIQUE,
    idCargo integer NOT NULL,
    PRIMARY KEY (idFuncionario),
    CONSTRAINT fk_funcionario_cargo FOREIGN KEY (idCargo) REFERENCES cargos (idCargo) ON DELETE CASCADE 
);

CREATE TABLE IF NOT EXISTS vendas
(
    idVenda SERIAL,
	idCliente integer NOT NULL,
	idFuncionario integer NOT NULL,
    dtCompra date,
    PRIMARY KEY (idVenda),
	CONSTRAINT fk_vendas_cliente FOREIGN KEY (idCliente) REFERENCES clientes (idCliente) ON DELETE CASCADE ,
	CONSTRAINT fk_vendas_funcionario FOREIGN KEY (idFuncionario) REFERENCES funcionarios (idFuncionario) ON DELETE CASCADE 
);

CREATE TABLE IF NOT EXISTS ingressos
(
    idIngresso SERIAL,
	idEvento integer NOT NULL,
	idVenda integer NOT NULL,
    valorIngresso DECIMAL(7, 2) NOT NULL,
    quantidade INT NOT NULL,
    PRIMARY KEY (idIngresso,idEvento,idVenda),
	CONSTRAINT fk_eventos FOREIGN KEY (idEvento) REFERENCES eventos (idEvento) ON DELETE CASCADE,
	CONSTRAINT fk_vendas FOREIGN KEY (idVenda) REFERENCES vendas (idVenda) ON DELETE CASCADE
);


INSERT INTO clientes (nome, email, telefone) VALUES
    ('Cliente 1', 'cliente1@example.com', '(47)-91111-1111'),
    ('Cliente 2', 'cliente2@example.com', '(47)-91111-1112'),
    ('Cliente 3', 'cliente3@example.com', '(47)-91111-1113'),
    ('Cliente 4', 'cliente4@example.com', '(47)-91111-1114'),
    ('Cliente 5', 'cliente5@example.com', '(47)-91111-1115');

INSERT INTO tipoeventos (descricao) VALUES
    ('Concerto'),
    ('Conferência'),
    ('Exposição'),
    ('Teatro'),
    ('Esporte');

INSERT INTO eventos (local, maxIngressos, data, idTipo) VALUES
    ('Local 1', 100, '2023-10-15', 1),
    ('Local 2', 200, '2023-11-20', 2),
    ('Local 3', 150, '2023-12-05', 3),
    ('Local 4', 50, '2023-10-30', 4),
    ('Local 5', 300, '2023-12-15', 5);

INSERT INTO cargos (descricao) VALUES
    ('Gerente'),
    ('Vendedor'),
    ('Atendente'),
    ('Técnico'),
    ('Analista');

INSERT INTO funcionarios (nome, email, idCargo) VALUES
    ('Funcionário 1', 'funcionario1@example.com', 1),
    ('Funcionário 2', 'funcionario2@example.com', 2),
    ('Funcionário 3', 'funcionario3@example.com', 2),
    ('Funcionário 4', 'funcionario4@example.com', 3),
    ('Funcionário 5', 'funcionario5@example.com', 4);


INSERT INTO vendas (idCliente, idFuncionario, dtCompra) VALUES
    (1, 1, '2023-10-16'),
    (2, 2, '2023-11-21'),
    (3, 3, '2023-12-06'),
    (4, 4, '2023-10-31'),
    (5, 5, '2023-12-16');


INSERT INTO ingressos (idEvento, idVenda, valorIngresso, quantidade) VALUES
    (1, 1, 50.00, 2),
    (2, 2, 30.00, 3),
    (3, 3, 25.00, 5),
    (4, 4, 40.00, 1),
    (5, 5, 20.00, 4);
