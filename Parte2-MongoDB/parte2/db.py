# -*- coding: utf-8 -*-
"""Conexión a MongoDB Atlas."""

from pymongo import MongoClient
from pymongo.database import Database

from config import load_config

_client: MongoClient | None = None


def get_database() -> Database:
    global _client
    cfg = load_config()
    if _client is None:
        _client = MongoClient(cfg["mongodb_uri"], serverSelectionTimeoutMS=15000)
        _client.admin.command("ping")
    return _client[cfg["database"]]


def close_connection() -> None:
    global _client
    if _client is not None:
        _client.close()
        _client = None
