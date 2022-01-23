
--
-- Database: estopa
--

use estopa;

-- --------------------------------------------------------
-- Trigger: Perfil del Comprador Y Vendedor
-- Al crear un nuevo usuario, en función del tipo se crea un registro en website_comprador o website_vendedor
-- --------------------------------------------------------
DELIMITER $$
CREATE TRIGGER website_usuario_insert AFTER INSERT ON website_usuario FOR EACH ROW
BEGIN
    IF NEW.tipo = 2 THEN
        INSERT INTO website_comprador(idUsuario_id) VALUES (NEW.id);
    ELSEIF NEW.tipo = 1 THEN
        INSERT INTO website_vendedor(idUsuario_id) VALUES (NEW.id);
    END IF;
END; $$



-- --------------------------------------------------------
-- Trigger: Perfil del Comprador Y Vendedor
-- Evita la modificación del tipo de un usuario.
-- --------------------------------------------------------
DELIMITER $$
CREATE TRIGGER website_usuario_tipo_update BEFORE UPDATE ON website_usuario FOR EACH ROW
BEGIN
    IF NEW.tipo <> OLD.tipo THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No se puede cambiar el campo tipo';
    END IF;
END; $$


-- --------------------------------------------------------
-- Trigger: Productos Usuario
-- Al confirmar un producto de un pedido (Pasar de estado 0 a 1), se le resta la cantidad del producto al inventario
-- --------------------------------------------------------
DELIMITER $$
CREATE TRIGGER website_productospedido_update AFTER UPDATE ON website_productospedido FOR EACH ROW
BEGIN
    IF NEW.estado = 1 AND OLD.estado = 0 THEN
        UPDATE website_producto SET cantidad = cantidad - NEW.cantidad WHERE website_producto.id = NEW.idProducto_id;
    END IF;
END; $$

-- --------------------------------------------------------
-- trigger: Productos Almacen
-- Al modificar un registro en la tabla website_producto evita que la cantidad sea negativa
-- --------------------------------------------------------
DELIMITER $$
CREATE TRIGGER website_producto_cantidad_update BEFORE UPDATE ON website_producto FOR EACH ROW
BEGIN
    IF NEW.cantidad < 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No se puede modificar la cantidad a un valor negativo';
    END IF;
END; $$


-- --------------------------------------------------------
-- Trigger: Compra
-- Comprueba que al insertar un producto en un pedido, existan existencias de dicho producto
-- --------------------------------------------------------
DELIMITER $$
CREATE TRIGGER website_productospedido_insert_stock BEFORE INSERT ON website_productospedido FOR EACH ROW
BEGIN
    set @CANT = (SELECT cantidad FROM website_producto WHERE website_producto.id = NEW.idProducto_id limit 1);
    IF @CANT < NEW.cantidad THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No hay stock suficiente';
    END IF;
END; $$


-- --------------------------------------------------------
-- Trigger: Gestion
-- Trigger que evite eliminar al usuario 0 (Administrador)
-- --------------------------------------------------------
DELIMITER $$
CREATE TRIGGER website_usuario_delete BEFORE DELETE ON website_usuario FOR EACH ROW
BEGIN
    IF OLD.id = 1 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No se puede eliminar al usuario 0';
    END IF;
END; $$


