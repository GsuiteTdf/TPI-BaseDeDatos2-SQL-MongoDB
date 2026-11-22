USE `cejas g - bd 2 - tp1`;

-- Limpieza previa para poder ejecutar el script desde cero
DROP TABLE IF EXISTS pedidos;
DROP TABLE IF EXISTS clientes;
DROP TABLE IF EXISTS productos;

-- Creación de la tabla PRODUCTOS
CREATE TABLE productos (
    id_producto INT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL
);

-- Creación de la tabla CLIENTES
CREATE TABLE clientes (
    id_cliente INT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    fecha_registro DATE NOT NULL
);

-- Creación de la tabla PEDIDOS con claves foráneas
CREATE TABLE pedidos (
    id_pedido INT PRIMARY KEY,
    cliente_id INT NOT NULL,
    producto_id INT NOT NULL,
    fecha DATE NOT NULL,
    total DECIMAL(10,2) NOT NULL,

    CONSTRAINT fk_pedidos_clientes
        FOREIGN KEY (cliente_id) REFERENCES clientes(id_cliente),

    CONSTRAINT fk_pedidos_productos
        FOREIGN KEY (producto_id) REFERENCES productos(id_producto)
);

-- Elaboración de la consigna a:
-- Inserte 1 cliente y 2 productos en sus respectivas tablas.

INSERT INTO clientes (id_cliente, nombre, email, fecha_registro)
VALUES (1, 'Ana Torres', 'ana.torres@gmail.com', '2026-04-29');

INSERT INTO productos (id_producto, nombre, precio, stock)
VALUES 
(1, 'Teclado Mecánico', 150.00, 10),
(2, 'Mouse Inalámbrico', 80.00, 20);

-- Inserción de pedidos de prueba para poder trabajar las consultas posteriores

INSERT INTO pedidos (id_pedido, cliente_id, producto_id, fecha, total)
VALUES
(1, 1, 1, '2026-05-10', 150.00),
(2, 1, 2, '2025-12-15', 80.00);

-- Elaboración de la consigna b:
-- Actualice el stock de uno de los productos insertados, estableciendo su valor en 5 unidades.

UPDATE productos
SET stock = 5
WHERE id_producto = 1;

-- Elaboración de la consigna c:
-- Elimine los pedidos cuya fecha sea anterior al año 2026.

DELETE FROM pedidos
WHERE id_pedido = 2;

-- Elaboración de la consigna d:
-- Liste todos los productos cuyo precio sea mayor a 100.

SELECT *
FROM productos
WHERE precio > 100;

-- Elaboración de la consigna e:
-- Muestre el nombre del cliente y la fecha de cada pedido.

SELECT c.nombre, p.fecha
FROM clientes AS c
INNER JOIN pedidos AS p
ON c.id_cliente = p.cliente_id;

-- Elaboración de la consigna f:
-- Obtenga la cantidad de pedidos por cliente.

SELECT c.nombre, COUNT(p.id_pedido) AS cantidad_pedidos
FROM clientes AS c
LEFT JOIN pedidos AS p
ON c.id_cliente = p.cliente_id
GROUP BY c.id_cliente, c.nombre;

-- Consultas finales de control para verificar el estado de las tablas

SELECT * FROM clientes;
SELECT * FROM productos;
SELECT * FROM pedidos;