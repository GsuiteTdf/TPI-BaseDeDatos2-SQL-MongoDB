# -*- coding: utf-8 -*-
"""
Food Store TPI - Parte 2
Aplicación de consola con operaciones CRUD sobre MongoDB Atlas.
"""

import sys
from datetime import datetime

import crud
from db import close_connection, get_database

COLLECTIONS = {
    "1": ("clientes", "Clientes"),
    "2": ("categorias", "Categorías"),
    "3": ("productos", "Productos"),
    "4": ("pedidos", "Pedidos"),
}


def pause() -> None:
    input("\nPresione Enter para continuar...")


def clear_screen() -> None:
    print("\n" * 2)


def read_line(prompt: str, required: bool = True) -> str:
    while True:
        value = input(prompt).strip()
        if value or not required:
            return value
        print("El campo no puede estar vacío.")


def read_float(prompt: str) -> float:
    while True:
        raw = read_line(prompt)
        try:
            return float(raw.replace(",", "."))
        except ValueError:
            print("Ingrese un número válido.")


def read_int(prompt: str) -> int:
    while True:
        raw = read_line(prompt)
        try:
            return int(raw)
        except ValueError:
            print("Ingrese un entero válido.")


def format_summary(collection_name: str, doc: dict) -> str:
    if collection_name == "clientes":
        return doc["nombre"]
    if collection_name == "categorias":
        return doc["nombre"]
    if collection_name == "productos":
        return doc["nombre"]
    if collection_name == "pedidos":
        cliente = doc.get("cliente_snapshot", {}).get("nombre", "Sin cliente")
        return f"{cliente} — ${doc.get('total', 0)} ({doc.get('estado', '')})"
    return str(doc.get("_id", ""))


def print_documents(collection_name: str, docs: list[dict], empty_message: str) -> None:
    if not docs:
        print(empty_message)
        return
    for index, doc in enumerate(docs, start=1):
        print(f"  {index}. {format_summary(collection_name, doc)}  (_id: {doc['_id']})")


def pick_document(collection_name: str, label: str) -> dict | None:
    docs = crud.read_all(get_database()[collection_name])
    if not docs:
        print(f"No hay {label} activos para seleccionar.")
        return None

    print_documents(collection_name, docs, "")
    doc_id = read_line(f"Ingrese el _id del {label[:-1] if label.endswith('s') else label}: ")
    doc = crud.read_by_id(get_database()[collection_name], doc_id)
    if not doc:
        print("No se encontró un registro activo con ese ID.")
    return doc


def handle_list(collection_name: str) -> None:
    docs = crud.read_all(get_database()[collection_name])
    total = crud.count_active(get_database()[collection_name])
    print(f"\nTotal activos en {collection_name}: {total}")
    print_documents(collection_name, docs, "No hay registros activos.")


def handle_create_cliente() -> None:
    db = get_database()
    doc = {
        "nombre": read_line("Nombre: "),
        "email": read_line("Email: "),
        "telefono": read_line("Teléfono: "),
        "direcciones": [
            {
                "tipo": read_line("Tipo de dirección (Casa/Trabajo): ", required=False) or "Casa",
                "calle": read_line("Calle: "),
                "numero": read_line("Número: "),
                "ciudad": read_line("Ciudad: "),
                "provincia": read_line("Provincia: "),
                "codigo_postal": read_line("Código postal: "),
                "principal": True,
            }
        ],
        "fecha_registro": datetime.now(),
    }
    new_id = crud.create(db.clientes, doc)
    print(f"Cliente creado con _id: {new_id}")


def handle_create_categoria() -> None:
    db = get_database()
    doc = {
        "nombre": read_line("Nombre: "),
        "descripcion": read_line("Descripción: "),
    }
    new_id = crud.create(db.categorias, doc)
    print(f"Categoría creada con _id: {new_id}")


def handle_create_producto() -> None:
    db = get_database()
    print("\nCategorías disponibles:")
    categorias = crud.read_all(db.categorias)
    print_documents("categorias", categorias, "Debe crear una categoría antes de un producto.")
    if not categorias:
        return

    categoria_id = read_line("ID de categoría: ")
    if not crud.read_by_id(db.categorias, categoria_id):
        print("Categoría no encontrada o inactiva.")
        return

    etiquetas_raw = read_line("Etiquetas separadas por coma: ", required=False)
    etiquetas = [tag.strip() for tag in etiquetas_raw.split(",") if tag.strip()]

    doc = {
        "nombre": read_line("Nombre: "),
        "descripcion": read_line("Descripción: "),
        "precio": read_float("Precio: "),
        "stock": read_int("Stock: "),
        "categoria_id": crud.parse_object_id(categoria_id),
        "etiquetas": etiquetas,
        "disponible": read_line("Disponible (s/n) [s]: ", required=False).lower() != "n",
    }
    new_id = crud.create(db.productos, doc)
    print(f"Producto creado con _id: {new_id}")


def handle_create_pedido() -> None:
    db = get_database()
    print("\nSeleccione cliente:")
    cliente = pick_document("clientes", "cliente")
    if not cliente:
        return

    items: list[dict] = []
    total = 0.0

    while True:
        print("\nSeleccione producto para agregar al pedido:")
        producto = pick_document("productos", "producto")
        if not producto:
            break

        cantidad = read_int("Cantidad: ")
        if cantidad <= 0:
            print("La cantidad debe ser mayor a cero.")
            continue

        precio = float(producto["precio"])
        subtotal = precio * cantidad
        items.append(
            {
                "producto_id": crud.parse_object_id(producto["_id"]),
                "nombre": producto["nombre"],
                "precio_unitario": precio,
                "cantidad": cantidad,
                "subtotal": subtotal,
            }
        )
        total += subtotal
        print(f"Subtotal parcial del pedido: ${total:.2f}")

        if read_line("¿Agregar otro producto? (s/n): ", required=False).lower() != "s":
            break

    if not items:
        print("El pedido debe tener al menos un producto.")
        return

    direccion = cliente["direcciones"][0] if cliente.get("direcciones") else {}
    doc = {
        "cliente_id": crud.parse_object_id(cliente["_id"]),
        "cliente_snapshot": {
            "nombre": cliente["nombre"],
            "email": cliente["email"],
            "telefono": cliente["telefono"],
        },
        "items": items,
        "total": total,
        "estado": read_line("Estado (pendiente/confirmado/entregado) [pendiente]: ", required=False) or "pendiente",
        "metodo_pago": read_line("Método de pago (efectivo/tarjeta/transferencia): "),
        "fecha_pedido": datetime.now(),
        "direccion_entrega": {
            "calle": direccion.get("calle") or read_line("Calle de entrega: "),
            "numero": direccion.get("numero") or read_line("Número de entrega: "),
            "ciudad": direccion.get("ciudad") or read_line("Ciudad de entrega: "),
            "provincia": direccion.get("provincia") or read_line("Provincia de entrega: "),
        },
    }
    new_id = crud.create(db.pedidos, doc)
    print(f"Pedido creado con _id: {new_id} | Total: ${total:.2f}")


def handle_update_cliente() -> None:
    db = get_database()
    doc_id = read_line("ID del cliente a modificar: ")
    if not crud.read_by_id(db.clientes, doc_id):
        print("Cliente no encontrado o inactivo.")
        return

    fields = {}
    for field in ("nombre", "email", "telefono"):
        value = read_line(f"Nuevo {field} (Enter para no cambiar): ", required=False)
        if value:
            fields[field] = value

    if crud.update(db.clientes, doc_id, fields):
        print("Cliente actualizado.")
    else:
        print("No se realizaron cambios.")


def handle_update_categoria() -> None:
    db = get_database()
    doc_id = read_line("ID de la categoría a modificar: ")
    if not crud.read_by_id(db.categorias, doc_id):
        print("Categoría no encontrada o inactiva.")
        return

    fields = {}
    for field in ("nombre", "descripcion"):
        value = read_line(f"Nuevo {field} (Enter para no cambiar): ", required=False)
        if value:
            fields[field] = value

    if crud.update(db.categorias, doc_id, fields):
        print("Categoría actualizada.")
    else:
        print("No se realizaron cambios.")


def handle_update_producto() -> None:
    db = get_database()
    doc_id = read_line("ID del producto a modificar: ")
    if not crud.read_by_id(db.productos, doc_id):
        print("Producto no encontrado o inactivo.")
        return

    fields = {}
    text_fields = ("nombre", "descripcion")
    for field in text_fields:
        value = read_line(f"Nuevo {field} (Enter para no cambiar): ", required=False)
        if value:
            fields[field] = value

    precio = read_line("Nuevo precio (Enter para no cambiar): ", required=False)
    if precio:
        fields["precio"] = float(precio.replace(",", "."))

    stock = read_line("Nuevo stock (Enter para no cambiar): ", required=False)
    if stock:
        fields["stock"] = int(stock)

    disponible = read_line("Disponible s/n (Enter para no cambiar): ", required=False)
    if disponible:
        fields["disponible"] = disponible.lower() == "s"

    if crud.update(db.productos, doc_id, fields):
        print("Producto actualizado.")
    else:
        print("No se realizaron cambios.")


def handle_update_pedido() -> None:
    db = get_database()
    doc_id = read_line("ID del pedido a modificar: ")
    if not crud.read_by_id(db.pedidos, doc_id):
        print("Pedido no encontrado o inactivo.")
        return

    fields = {}
    for field in ("estado", "metodo_pago"):
        value = read_line(f"Nuevo {field} (Enter para no cambiar): ", required=False)
        if value:
            fields[field] = value

    if crud.update(db.pedidos, doc_id, fields):
        print("Pedido actualizado.")
    else:
        print("No se realizaron cambios.")


def handle_logical_delete(collection_name: str) -> None:
    db = get_database()
    doc_id = read_line(f"ID del registro a dar de baja en {collection_name}: ")
    motivo = read_line("Motivo de baja: ", required=False)

    if crud.logical_delete(db[collection_name], doc_id, motivo):
        print("Baja lógica aplicada correctamente.")
    else:
        print("No se encontró un registro activo con ese ID.")


CREATE_HANDLERS = {
    "clientes": handle_create_cliente,
    "categorias": handle_create_categoria,
    "productos": handle_create_producto,
    "pedidos": handle_create_pedido,
}

UPDATE_HANDLERS = {
    "clientes": handle_update_cliente,
    "categorias": handle_update_categoria,
    "productos": handle_update_producto,
    "pedidos": handle_update_pedido,
}


def collection_menu(collection_name: str, label: str) -> None:
    while True:
        clear_screen()
        print(f"=== {label} ===")
        print("1. Listar (READ)")
        print("2. Crear (CREATE)")
        print("3. Modificar (UPDATE)")
        print("4. Baja lógica (DELETE)")
        print("0. Volver")

        option = read_line("\nOpción: ")
        try:
            if option == "1":
                handle_list(collection_name)
            elif option == "2":
                CREATE_HANDLERS[collection_name]()
            elif option == "3":
                UPDATE_HANDLERS[collection_name]()
            elif option == "4":
                handle_logical_delete(collection_name)
            elif option == "0":
                return
            else:
                print("Opción inválida.")
        except ValueError as exc:
            print(f"Error: {exc}")
        except Exception as exc:
            print(f"Error inesperado: {exc}")

        pause()


def main_menu() -> None:
    while True:
        clear_screen()
        print("=" * 48)
        print("  FOOD STORE TPI - Parte 2 (CRUD + MongoDB Atlas)")
        print("=" * 48)
        for key, (_, label) in COLLECTIONS.items():
            print(f"{key}. {label}")
        print("0. Salir")

        option = read_line("\nOpción: ")
        if option == "0":
            print("Cerrando aplicación...")
            break
        if option in COLLECTIONS:
            collection_name, label = COLLECTIONS[option]
            collection_menu(collection_name, label)
        else:
            print("Opción inválida.")
            pause()


def main() -> None:
    try:
        get_database()
        print("Conexión exitosa a MongoDB Atlas.\n")
        pause()
        main_menu()
    except FileNotFoundError as exc:
        print(exc)
        sys.exit(1)
    except Exception as exc:
        print(f"No se pudo conectar a MongoDB Atlas: {exc}")
        sys.exit(1)
    finally:
        close_connection()


if __name__ == "__main__":
    main()
