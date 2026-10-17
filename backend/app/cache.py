import sqlite3
from pathlib import Path
from .schemas import Blueprint


class BlueprintCache:
    def __init__(self, path: str = "tiny_wonders.db") -> None:
        self.path = Path(path)
        with self._connection() as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS blueprints (slug TEXT PRIMARY KEY, json TEXT NOT NULL, created_at TEXT DEFAULT CURRENT_TIMESTAMP)")

    def _connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.path)

    def get(self, slug: str) -> Blueprint | None:
        with self._connection() as conn:
            row = conn.execute("SELECT json FROM blueprints WHERE slug = ?", (slug,)).fetchone()
        return Blueprint.model_validate_json(row[0]) if row else None

    def put(self, blueprint: Blueprint) -> None:
        with self._connection() as conn:
            conn.execute("INSERT OR REPLACE INTO blueprints(slug, json) VALUES (?, ?)", (blueprint.slug, blueprint.model_dump_json()))
