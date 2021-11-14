-- Script to create database

--CREATE DATABASE estopa;

--USE estopa;

-- Disable autocommit
SET autocommit = 0;

DROP TABLE detalle_pedido;
DROP TABLE stock;
DROP TABLE pedido;


CREATE TABLE stock (
	Cproducto int PRIMARY KEY AUTO_INCREMENT,
    Cantidad int NOT NULL
);

CREATE TABLE pedido (
	Cpedido int PRIMARY KEY AUTO_INCREMENT,
    Ccliente int NOT NULL,
    FechaPedido date NOT NULL
);

CREATE TABLE detalle_pedido (
	Cpedido int NOT NULL,
    Cproducto int NOT NULL,
    Cantidad int NOT NULL,
    FOREIGN KEY (Cpedido) REFERENCES pedido(Cpedido),
    FOREIGN KEY (Cproducto) REFERENCES stock(Cproducto)
);

-- Create user & set privileges
--CREATE USER 'estopa'@'%' IDENTIFIED BY 'estopa';
--GRANT ALL PRIVILEGES ON estopa.* 'estopa'@'0.0.0.0' WITH GRANT OPTION;

--FLUSH PRIVILEGES;