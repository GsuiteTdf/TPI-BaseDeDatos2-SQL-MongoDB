# Food Store TPI – Parte 2

Trabajo Práctico Integrador de **Bases de Datos II** (UTN).  
Aplicación de consola con operaciones CRUD sobre MongoDB Atlas y script de resguardo con `mongodump`.

**Dominio:** Food Store – tienda online de productos gastronómicos.  
**Base de datos:** `foodstore_tpi`  
**Colecciones:** `clientes`, `categorias`, `productos`, `pedidos`


## Requisitos previos

- **Python 3.10+**
- **MongoDB Atlas** con el clúster y la base de datos de la Parte 1
- **MongoDB Database Tools** (para el backup): [descarga](https://www.mongodb.com/try/download/database-tools)  
  Verificar instalación:
  ```powershell
  mongodump --version
  ```

1. Descripción general

Este proyecto corresponde a la segunda parte del Trabajo Práctico Integrador de la asignatura Bases de Datos II.

El objetivo es conectar una aplicación desarrollada en Python con una base de datos MongoDB alojada en MongoDB Atlas, realizar operaciones CRUD sobre los documentos y aplicar una estrategia básica de respaldo mediante la herramienta mongodump.

La aplicación fue desarrollada como un programa de consola. Se priorizó una implementación sencilla y funcional, sin incorporar arquitecturas de software innecesariamente complejas.

El proyecto permite realizar las siguientes operaciones:

Crear nuevos documentos.
Consultar documentos activos.
Actualizar campos específicos.
Aplicar una baja lógica sin borrar físicamente los documentos.
Generar un respaldo de la base de datos almacenada en MongoDB Atlas.
2. Tecnologías utilizadas
Python 3.
MongoDB Atlas.
PyMongo.
MongoDB Database Tools.
mongodump.
PowerShell.
Símbolo del sistema de Windows.
Windows 11.
3. Estructura del proyecto
Parte2-MongoDB/
│
├── backup_tpi.bat
├── backup_tpi.ps1
│
└── parte2/
    ├── README.md
    ├── main.py
    ├── crud.py
    ├── db.py
    ├── config.py
    ├── config.example.json
    └── requirements.txt

La carpeta resguardos_tpi no se incluye inicialmente en la entrega, ya que es creada automáticamente cuando se ejecuta el script de backup.

Después de realizar un respaldo, la estructura será similar a la siguiente:

Parte2-MongoDB/
│
├── resguardos_tpi/
│   └── AAAA-MM-DD/
│       └── foodstore_tpi/
│           ├── clientes.bson
│           ├── pedidos.bson
│           ├── productos.bson
│           └── categorias.bson
│
├── backup_tpi.bat
├── backup_tpi.ps1
│
└── parte2/

El contenido exacto del respaldo puede variar según las colecciones existentes en la base de datos.

4. Descripción de los archivos
main.py

Contiene el menú principal de la aplicación y permite al usuario seleccionar las diferentes operaciones disponibles.

Desde este archivo se coordinan las acciones de creación, lectura, modificación y baja lógica de los documentos.

crud.py

Contiene las funciones encargadas de ejecutar las operaciones CRUD sobre MongoDB:

create(): inserta un nuevo documento.
read_all(): obtiene los documentos activos.
read_by_id(): busca un documento activo por su identificador.
update(): modifica campos específicos.
soft_delete(): aplica la baja lógica.
db.py

Gestiona la conexión con MongoDB Atlas mediante MongoClient.

También realiza una operación ping para verificar que la conexión con el clúster se haya establecido correctamente.

config.py

Lee y valida los datos de configuración necesarios para conectar la aplicación con MongoDB Atlas.

config.example.json

Archivo de ejemplo que contiene la estructura que debe tener la configuración local.

No contiene credenciales reales.

requirements.txt

Contiene las dependencias de Python necesarias para ejecutar el proyecto.

backup_tpi.bat

Archivo ejecutable para Windows que inicia el script de PowerShell encargado de generar el backup.

backup_tpi.ps1

Script de PowerShell que:

Obtiene la fecha actual.
Crea la carpeta resguardos_tpi.
Crea una subcarpeta con la fecha actual.
Lee la conexión desde parte2\config.json.
Ejecuta mongodump.
Guarda el respaldo dentro de la carpeta correspondiente.
5. Requisitos previos

Para ejecutar el proyecto se necesita:

Windows 11.
Python 3 instalado.
Acceso a un clúster de MongoDB Atlas.
MongoDB Database Tools instalado.
La herramienta mongodump disponible desde la terminal.
Una conexión a Internet.
La dirección IP autorizada en MongoDB Atlas.

Para verificar la instalación de Python, ejecutar:

python --version

Para verificar que mongodump esté disponible, ejecutar:

mongodump --version

Si ambos comandos muestran una versión instalada, el entorno se encuentra preparado.

6. Configuración de MongoDB Atlas

Antes de ejecutar la aplicación se debe crear un archivo local llamado:

config.json

Este archivo debe ubicarse dentro de:

Parte2-MongoDB\parte2

Puede crearse copiando el archivo de ejemplo.

Desde CMD:

cd Parte2-MongoDB\parte2
copy config.example.json config.json

Desde PowerShell:

cd Parte2-MongoDB\parte2
Copy-Item config.example.json config.json

Luego debe editarse config.json y reemplazar los valores de ejemplo por los datos reales del clúster:

{
  "mongodb_uri": "mongodb+srv://USUARIO:CONTRASEÑA@CLUSTER.mongodb.net/?retryWrites=true&w=majority",
  "database": "foodstore_tpi"
}

Se deben reemplazar:

USUARIO: usuario configurado en MongoDB Atlas.
CONTRASEÑA: contraseña del usuario.
CLUSTER: dirección correspondiente al clúster.
foodstore_tpi: nombre de la base de datos, si fuera diferente.
Importante sobre las credenciales

El archivo config.json contiene información privada y no debe incluirse en repositorios públicos ni compartirse dentro del archivo ZIP de entrega.

La entrega debe contener solamente:

config.example.json

Cada usuario debe crear su propio config.json de manera local.

7. Instalación de dependencias

Abrir CMD o PowerShell y acceder a la carpeta de la aplicación:

cd Parte2-MongoDB\parte2

Instalar las dependencias:

pip install -r requirements.txt

La dependencia principal es:

pymongo

PyMongo permite establecer la comunicación entre la aplicación desarrollada en Python y el clúster de MongoDB Atlas.

8. Ejecución de la aplicación

Desde la carpeta:

Parte2-MongoDB\parte2

ejecutar:

python main.py

La aplicación intentará conectarse con MongoDB Atlas.

Si la conexión es correcta, se mostrará un mensaje de confirmación y aparecerá el menú principal.

9. Operaciones CRUD implementadas
9.1 CREATE — Inserción

La operación CREATE permite registrar nuevos documentos en las colecciones del dominio.

La inserción se realiza mediante:

collection.insert_one(document)

Al crear un documento se agregan también los campos necesarios para administrar la baja lógica.

Ejemplo conceptual:

{
  "nombre": "Producto de ejemplo",
  "precio": 1500,
  "stock": 10,
  "eliminado": false,
  "fecha_eliminacion": null,
  "motivo_eliminacion": null
}
9.2 READ — Lectura

La operación READ recupera los documentos almacenados en MongoDB.

Para respetar la baja lógica, las consultas normales incluyen el siguiente filtro:

{"eliminado": False}

De esta manera, los documentos desactivados no se muestran en los listados de la aplicación.

La consulta se realiza mediante:

collection.find({"eliminado": False})

También es posible buscar un documento activo por su _id.

9.3 UPDATE — Modificación

La operación UPDATE permite modificar únicamente campos específicos de un documento existente.

La actualización se realiza mediante el operador:

{"$set": campos_actualizados}

Ejemplo:

collection.update_one(
    {"_id": identificador, "eliminado": False},
    {"$set": {"precio": 2500, "stock": 20}}
)

Los campos internos vinculados con el identificador y la baja lógica no pueden modificarse desde la operación común de actualización.

9.4 DELETE — Baja lógica

La operación DELETE no elimina físicamente el documento de MongoDB.

En su lugar, modifica su estado mediante los siguientes campos:

{
  "eliminado": true,
  "fecha_eliminacion": "fecha y hora de la baja",
  "motivo_eliminacion": "motivo informado"
}

La operación se realiza mediante $set:

collection.update_one(
    {"_id": identificador, "eliminado": False},
    {
        "$set": {
            "eliminado": True,
            "fecha_eliminacion": fecha_actual,
            "motivo_eliminacion": motivo
        }
    }
)

Esta estrategia conserva el documento en la base de datos y permite mantener su historial.

10. Ejecución del backup

El respaldo se realiza mediante los archivos:

backup_tpi.bat
backup_tpi.ps1

El archivo .bat inicia automáticamente el script de PowerShell.

Procedimiento

Abrir CMD y acceder a la carpeta raíz de la Parte 2:

cd Parte2-MongoDB

Ejecutar:

backup_tpi.bat

También puede ejecutarse desde PowerShell:

.\backup_tpi.bat

El script leerá la configuración ubicada en:

parte2\config.json

Luego creará una carpeta con la siguiente estructura:

resguardos_tpi\AAAA-MM-DD

Por ejemplo:

resguardos_tpi\2026-06-27

Dentro de esa carpeta se almacenará el respaldo generado por mongodump.

11. Funcionamiento del script de backup

El script utiliza la ruta donde se encuentra almacenado el propio archivo mediante:

$PSScriptRoot

Esto permite trabajar con rutas relativas, sin depender de una ubicación absoluta específica del equipo.

La fecha se obtiene mediante:

Get-Date -Format "yyyy-MM-dd"

La carpeta de destino se construye con:

$destino = ".\resguardos_tpi\$fecha"

La creación de la carpeta se realiza con:

New-Item -ItemType Directory -Force -Path $destino

Finalmente, el respaldo se genera mediante:

mongodump --uri="URI_DE_MONGODB_ATLAS" --db="foodstore_tpi" --out="$destino"

El script comprueba también el código de salida de mongodump para informar si la operación finalizó correctamente o si ocurrió un error.

12. Resultado esperado del backup

Cuando el procedimiento finaliza correctamente, la consola muestra un mensaje similar a:

Resguardo completado correctamente.
Ubicación: resguardos_tpi\2026-06-27

Dentro de la carpeta generada se encontrarán archivos con extensión:

.bson
.metadata.json

Los archivos .bson contienen los documentos almacenados en cada colección.

Los archivos .metadata.json contienen información relacionada con la estructura y los índices de las colecciones.

13. Restauración del respaldo

Aunque la consigna principal solicita generar el backup con mongodump, el respaldo puede restaurarse posteriormente mediante mongorestore.

Ejemplo general:

mongorestore --uri="URI_DE_MONGODB_ATLAS" --db="foodstore_tpi" "resguardos_tpi\AAAA-MM-DD\foodstore_tpi"

Antes de realizar una restauración sobre una base de datos real se recomienda probar el procedimiento en un entorno de prueba.

14. RPO y RTO
RPO — Recovery Point Objective

El RPO determina la cantidad máxima de información que la organización puede aceptar perder, medida como un período de tiempo.

Si se realiza un backup una vez por día, el RPO máximo estimado es de 24 horas.

Esto significa que, ante una falla, podrían perderse los datos generados desde el último respaldo exitoso.

RTO — Recovery Time Objective

El RTO determina el tiempo máximo aceptable para recuperar la base de datos y restablecer el funcionamiento del servicio.

Para este proyecto se estima:

Localización y preparación del respaldo: entre 5 y 15 minutos.
Restauración mediante mongorestore: entre 5 y 20 minutos.
Verificación de la base de datos y la aplicación: entre 5 y 10 minutos.

Por lo tanto, el RTO total estimado es de entre 15 y 45 minutos, sin contar el tiempo variable requerido para detectar inicialmente el incidente.

15. Consideraciones de seguridad
No incluir config.json en el archivo ZIP de entrega.
No publicar usuarios ni contraseñas de MongoDB Atlas.
Utilizar config.example.json como plantilla.
Autorizar únicamente las direcciones IP necesarias en Atlas.
Utilizar un usuario de MongoDB con permisos limitados al proyecto.
Cambiar inmediatamente cualquier contraseña que haya sido compartida accidentalmente.
No publicar respaldos que contengan información sensible.
16. Errores frecuentes
Python no se reconoce como comando

Verificar la instalación:

python --version

Si no funciona, reinstalar Python y seleccionar la opción para agregarlo al PATH.

No se encuentra el módulo pymongo

Ejecutar:

pip install -r requirements.txt
Error de autenticación en MongoDB Atlas

Revisar:

Usuario.
Contraseña.
URI del clúster.
Nombre de la base.
Permisos del usuario.
Error de conexión o timeout

Verificar que la dirección IP esté autorizada en MongoDB Atlas.

mongodump no se reconoce como comando

Instalar MongoDB Database Tools y agregar su carpeta bin a la variable de entorno PATH.

Verificar nuevamente:

mongodump --version
No se encuentra config.json

Crear el archivo a partir de:

config.example.json

y ubicarlo en:

Parte2-MongoDB\parte2\config.json
17. Conclusión

La realización de esta segunda parte del TPI permitió integrar una aplicación real con un motor de base de datos NoSQL alojado en la nube.

La aplicación actúa como cliente y envía solicitudes al clúster de MongoDB Atlas a través de PyMongo. MongoDB procesa las operaciones y devuelve los resultados correspondientes.

La implementación de operaciones CREATE, READ, UPDATE y DELETE lógico permitió comprender el ciclo de vida de los documentos y la importancia de conservar la integridad de la información.

La baja lógica evita eliminar físicamente los registros y permite mantener su historial. Por su parte, el uso de mongodump permite generar respaldos independientes que pueden utilizarse ante pérdidas de datos o fallas del sistema.

Uno de los principales desafíos fue gestionar correctamente la conexión remota, las credenciales, los identificadores ObjectId y los filtros necesarios para excluir los documentos eliminados lógicamente.

La experiencia permitió comprender de forma práctica el flujo de comunicación cliente-servidor, desde la solicitud realizada por la aplicación hasta el procesamiento y almacenamiento de la información en MongoDB Atlas.

