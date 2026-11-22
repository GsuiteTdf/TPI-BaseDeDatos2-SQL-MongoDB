# -*- coding: utf-8 -*-
"""Operaciones CRUD con baja lógica para Food Store TPI."""

from datetime import datetime, timezone
from typing import Any

from bson import ObjectId
from bson.errors import InvalidId
from pymongo.collection import Collection

ACTIVE_FILTER = {"eliminado": False}


def _soft_delete_fields() -> dict:
    return {
        "eliminado": False,
        "fecha_eliminacion": None,
        "motivo_eliminacion": None,
    }


def parse_object_id(value: str) -> ObjectId:
    try:
        return ObjectId(value.strip())
    except InvalidId as exc:
        raise ValueError(f"ID inválido: {value}") from exc


def serialize(value: Any) -> Any:
    if isinstance(value, ObjectId):
        return str(value)
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d %H:%M:%S")
    if isinstance(value, list):
        return [serialize(item) for item in value]
    if isinstance(value, dict):
        return {key: serialize(val) for key, val in value.items()}
    return value


def create(collection: Collection, document: dict) -> str:
    doc = {**document, **_soft_delete_fields()}
    result = collection.insert_one(doc)
    return str(result.inserted_id)


def read_all(collection: Collection, extra_filter: dict | None = None) -> list[dict]:
    query = {**ACTIVE_FILTER}
    if extra_filter:
        query.update(extra_filter)
    docs = list(collection.find(query))
    return [serialize(doc) for doc in docs]


def read_by_id(collection: Collection, doc_id: str) -> dict | None:
    query = {"_id": parse_object_id(doc_id), **ACTIVE_FILTER}
    doc = collection.find_one(query)
    return serialize(doc) if doc else None


def update(collection: Collection, doc_id: str, fields: dict) -> bool:
    forbidden = {"_id", "activo", "eliminado", "fecha_eliminacion", "motivo_eliminacion"}
    updates = {k: v for k, v in fields.items() if k not in forbidden}
    if not updates:
        return False

    result = collection.update_one(
        {"_id": parse_object_id(doc_id), **ACTIVE_FILTER},
        {"$set": updates},
    )
    return result.modified_count > 0


def logical_delete(collection: Collection, doc_id: str, motivo: str) -> bool:
    result = collection.update_one(
        {"_id": parse_object_id(doc_id), **ACTIVE_FILTER},
        {
            "$set": {
                "eliminado": True,
                "fecha_eliminacion": datetime.now(timezone.utc),
                "motivo_eliminacion": motivo.strip() or "Baja lógica desde aplicación",
            }
        },
    )
    return result.modified_count > 0


def count_active(collection: Collection) -> int:
    return collection.count_documents(ACTIVE_FILTER)
