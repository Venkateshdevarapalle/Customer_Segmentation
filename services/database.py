"""Persistent storage used by CustomerIQ.

Default: SQLite, so the application runs immediately without another service.
Production option: set DATABASE_URL to a PostgreSQL connection string.
"""
from __future__ import annotations

import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
DEFAULT_DB = BASE / "data" / "customeriq.db"


def _is_postgres() -> bool:
    return os.getenv("DATABASE_URL", "").lower().startswith(("postgres://", "postgresql://"))


def _connect():
    if _is_postgres():
        try:
            import psycopg
        except ImportError as exc:
            raise RuntimeError("PostgreSQL is configured but psycopg is not installed. Run pip install -r requirements.txt.") from exc
        return psycopg.connect(os.environ["DATABASE_URL"])
    DEFAULT_DB.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DEFAULT_DB)


def _sql(sql: str) -> str:
    return sql.replace("?", "%s") if _is_postgres() else sql


def _id_type() -> str:
    return "SERIAL PRIMARY KEY" if _is_postgres() else "INTEGER PRIMARY KEY AUTOINCREMENT"


def initialize_database() -> None:
    conn = _connect()
    try:
        cur = conn.cursor()
        ident = _id_type()
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS model_runs (
                id {ident},
                model_version TEXT NOT NULL,
                algorithm TEXT NOT NULL,
                clusters INTEGER NOT NULL,
                features INTEGER NOT NULL,
                silhouette REAL,
                davies_bouldin REAL,
                calinski_harabasz REAL,
                trained_at TEXT NOT NULL
            )
        """)
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS prediction_logs (
                id {ident},
                age INTEGER NOT NULL,
                income_lakh REAL NOT NULL,
                annual_spending REAL NOT NULL,
                average_order_value REAL NOT NULL,
                predicted_segment TEXT NOT NULL,
                confidence REAL NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS uploaded_datasets (
                id {ident},
                filename TEXT NOT NULL,
                rows_count INTEGER NOT NULL,
                columns_count INTEGER NOT NULL,
                segmented INTEGER NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        conn.commit()
    finally:
        conn.close()


def save_model_run(metrics: dict[str, float], features: int, clusters: int = 5, version: str = "v1.1") -> None:
    initialize_database()
    conn = _connect()
    try:
        conn.cursor().execute(
            _sql("INSERT INTO model_runs (model_version,algorithm,clusters,features,silhouette,davies_bouldin,calinski_harabasz,trained_at) VALUES (?,?,?,?,?,?,?,?)"),
            (version, "K-Means", clusters, features, metrics["silhouette"], metrics["davies_bouldin"], metrics["calinski_harabasz"], datetime.now(timezone.utc).isoformat()),
        )
        conn.commit()
    finally:
        conn.close()


def log_prediction(age: int, income_lakh: float, annual_spending: float, aov: float, segment: str, confidence: float) -> None:
    initialize_database()
    conn = _connect()
    try:
        conn.cursor().execute(
            _sql("INSERT INTO prediction_logs (age,income_lakh,annual_spending,average_order_value,predicted_segment,confidence,created_at) VALUES (?,?,?,?,?,?,?)"),
            (int(age), float(income_lakh), float(annual_spending), float(aov), segment, float(confidence), datetime.now(timezone.utc).isoformat()),
        )
        conn.commit()
    finally:
        conn.close()


def log_upload(filename: str, rows: int, columns: int, segmented: bool) -> None:
    initialize_database()
    conn = _connect()
    try:
        conn.cursor().execute(
            _sql("INSERT INTO uploaded_datasets (filename,rows_count,columns_count,segmented,created_at) VALUES (?,?,?,?,?)"),
            (filename, int(rows), int(columns), int(segmented), datetime.now(timezone.utc).isoformat()),
        )
        conn.commit()
    finally:
        conn.close()
