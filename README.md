# Base de Datos II — Food Store: SQL relacional y MongoDB

Trabajo Práctico Integrador · Bases de Datos II · Tecnicatura Universitaria en Programación a Distancia (UTN).

Dos partes sobre el mismo dominio (Food Store, tienda de productos gastronómicos): primero un modelo **relacional en MySQL** con integridad referencial, y luego una **aplicación de consola en Python** que trabaja sobre **MongoDB Atlas** con operaciones CRUD, baja lógica y respaldos automatizados con `mongodump`.

- **Grupo 159**
- **Integrantes:** Gastón Cejas · Claudio Rodríguez

## Stack

| Parte   | Tecnologías                                                                 |
| ------- | --------------------------------------------------------------------------- |
| Parte 1 | MySQL · SQL (DDL / DML) · integridad referencial                            |
| Parte 2 | Python 3.10+ · PyMongo · MongoDB Atlas · MongoDB Database Tools · PowerShell |

## Estructura

```
.
├── Parte1-SQL/
│   ├── BD2 - TP1 - Ejercicio 1 - Creacion de las Tablas.sql   tablas PRODUCTOS, CLIENTES y PEDIDOS con PK y FK
│   └── BD2 - TP1 - Ejercicio 1.sql                            versión idempotente (DROP previo) con datos de ejemplo
└── Parte2-MongoDB/
    ├── backup_tpi.bat        lanza el respaldo en Windows
    ├── backup_tpi.ps1        respaldo con mongodump en una carpeta por fecha
    └── parte2/
        ├── main.py           menú de consola
        ├── crud.py           create, read_all, read_by_id, update y soft_delete
        ├── db.py             conexión con MongoClient y ping al clúster
        ├── config.py         lectura y validación de la configuración
        ├── config.example.json
        ├── requirements.txt
        └── README.md         guía detallada de la Parte 2
```

## Parte 1 — Modelo relacional (MySQL)

Ejecutar en MySQL los scripts de `Parte1-SQL/`. Crean las tablas `productos`, `clientes` y `pedidos` asegurando la integridad referencial (claves primarias, foráneas, `NOT NULL` y `UNIQUE`) y cargan datos de ejemplo.

## Parte 2 — Aplicación Python + MongoDB Atlas

### 1. Instalación

```bash
cd Parte2-MongoDB/parte2
pip install -r requirements.txt
```

### 2. Configuración

Copiar la plantilla y completar los datos del clúster:

```bash
# Windows
copy config.example.json config.json
# Linux / macOS
cp config.example.json config.json
```

| Clave         | Descripción                    | Ejemplo                                                                  |
| ------------- | ------------------------------ | ------------------------------------------------------------------------ |
| `mongodb_uri` | Cadena de conexión de Atlas    | `mongodb+srv://USUARIO:CONTRASEÑA@CLUSTER.mongodb.net/?retryWrites=true` |
| `database`    | Base de datos                  | `foodstore_tpi`                                                          |

> `config.json` contiene credenciales y está excluido del repositorio en `.gitignore`.

### 3. Ejecución

```bash
python main.py
```

Colecciones: `clientes`, `categorias`, `productos` y `pedidos`.

| Operación | Implementación                                                                                 |
| --------- | ---------------------------------------------------------------------------------------------- |
| CREATE    | `insert_one`, agregando los campos de baja lógica                                              |
| READ      | `find({"eliminado": False})` y búsqueda de documentos activos por `_id`                        |
| UPDATE    | `update_one` con `$set` solo sobre campos editables                                            |
| DELETE    | Baja lógica: `eliminado`, `fecha_eliminacion` y `motivo_eliminacion` (no se borra el documento) |

### 4. Respaldo

```bash
cd Parte2-MongoDB
backup_tpi.bat
```

Genera `resguardos_tpi/AAAA-MM-DD/foodstore_tpi/` con un archivo `.bson` y su `.metadata.json` por colección. Se restaura con `mongorestore`.

| Indicador | Estimación                     |
| --------- | ------------------------------ |
| RPO       | 24 horas (un respaldo diario)  |
| RTO       | Entre 15 y 45 minutos           |

El detalle completo (restauración, seguridad y errores frecuentes) está en [`Parte2-MongoDB/parte2/README.md`](Parte2-MongoDB/parte2/README.md).
