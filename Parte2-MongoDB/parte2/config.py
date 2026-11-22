# -*- coding: utf-8 -*-
"""Configuración de conexión a MongoDB Atlas."""

import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CONFIG_FILE = BASE_DIR / "config.json"

DEFAULT_DATABASE = "foodstore_tpi"


def load_config() -> dict:
    if CONFIG_FILE.exists():
        with CONFIG_FILE.open(encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}

    uri = os.getenv("MONGODB_URI") or data.get("mongodb_uri")
    database = os.getenv("MONGODB_DATABASE") or data.get("database", DEFAULT_DATABASE)

    if not uri:
        raise FileNotFoundError(
            "No se encontró la URI de MongoDB.\n"
            f"Cree {CONFIG_FILE.name} a partir de config.example.json "
            "o defina la variable de entorno MONGODB_URI."
        )

    return {"mongodb_uri": uri, "database": database}
