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


