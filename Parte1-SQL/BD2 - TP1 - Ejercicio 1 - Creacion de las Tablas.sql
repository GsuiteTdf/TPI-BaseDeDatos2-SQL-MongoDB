-- Seleccionamos el esquema/base de datos donde vamos a trabajar
USE `cejas g - bd 2 - tp1`;

-- ============================================================
-- PASO 1: Crear la tabla PRODUCTOS
-- Consigna: PRODUCTOS (id_producto, nombre, precio, stock)
-- ============================================================

CREATE TABLE productos (
    id_producto INT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL
);

-- ============================================================
-- PASO 2: Crear la tabla CLIENTES
-- Consigna: CLIENTES (id_cliente, nombre, email, fecha_registro)
-- ============================================================

CREATE TABLE clientes (
    id_cliente INT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    fecha_registro DATE NOT NULL
);

-- ============================================================
-- PASO 3: Crear la tabla PEDIDOS
-- Consigna original: PEDIDOS (id_pedido, cliente_id, fecha, total)
-- Mejora solicitada: incorporar producto_id como clave foránea
-- para vincular cada pedido con un producto.
-- ============================================================

CREATE TABLE pedidos (
    id_pedido INT PRIMARY KEY,
    cliente_id INT NOT NULL,
    producto_id INT NOT NULL,
    fecha DATE NOT NULL,
    total DECIMAL(10,2) NOT NULL,

    -- Clave foránea que vincula cada pedido con un cliente existente
    CONSTRAINT fk_pedidos_clientes
        FOREIGN KEY (cliente_id)
        REFERENCES clientes(id_cliente),

    -- Clave foránea que vincula cada pedido con un producto existente
    CONSTRAINT fk_pedidos_productos
        FOREIGN KEY (producto_id)
        REFERENCES productos(id_producto)
);

-- ============================================================
-- PASO 4: Insertar un cliente
-- Se carga un registro en la tabla CLIENTES.
-- ============================================================

INSERT INTO clientes (id_cliente, nombre, email, fecha_registro)
VALUES (1, 'Ana Torres', 'ana.torres@gmail.com', '2026-04-29');

-- ============================================================
-- PASO 5: Insertar dos productos
-- Se cargan dos registros en la tabla PRODUCTOS.
-- ============================================================

INSERT INTO productos (id_producto, nombre, precio, stock)
VALUES 
(1, 'Teclado Mecánico', 150.00, 10),
(2, 'Mouse Inalámbrico', 80.00, 20);

-- ============================================================
-- PASO 6: Insertar pedidos de prueba
-- Se cargan pedidos vinculados al cliente y a los productos.
-- Esto respeta la integridad referencial, porque:
-- cliente_id = 1 existe en CLIENTES.
-- producto_id = 1 y producto_id = 2 existen en PRODUCTOS.
-- ============================================================

INSERT INTO pedidos (id_pedido, cliente_id, producto_id, fecha, total)
VALUES
(1, 1, 1, '2026-05-10', 150.00),
(2, 1, 2, '2025-12-15', 80.00);

-- ============================================================
-- PASO 7: Verificar los datos cargados
-- Estas consultas permiten comprobar que las tres tablas
-- fueron creadas correctamente y contienen registros.
-- ============================================================

SELECT * FROM clientes;
SELECT * FROM productos;
SELECT * FROM pedidos;