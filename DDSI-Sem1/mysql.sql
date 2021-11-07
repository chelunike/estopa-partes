-- Script to create database

CREATE DATABASE estopaBD;

USE estopaBD;

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



CREATE USER 'admin'@'localhost' IDENTIFIED BY 'admin';
GRANT ALL PRIVILEGES ON *.* TO 'admin'@'0.0.0.0' WITH GRANT OPTION;
FLUSH PRIVILEGES;