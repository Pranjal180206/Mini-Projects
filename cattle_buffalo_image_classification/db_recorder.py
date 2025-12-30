import sqlite3
from datetime import datetime
from pathlib import Path

db_Path = Path("classification_records.db")

def get_db_conn():
    return sqlite3.connect(db_Path)

def init_db():
    conn = get_db_conn()
    cursor = conn.cursor()

    cursor.execute("""
                CREATE TABLE IF NOT EXISTS classification_records (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   timestamp TEXT NOT NULL,
                   img_name TEXT NOT NULL,
                   pred_class TEXT NOT NULL,
                   confidence REAL NOT NULL
                   )
    """)

    conn.commit()
    conn.close()

def record_classification(img_name, pred_class, confidence):
    conn = get_db_conn()
    cursor = conn.cursor()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
                INSERT INTO classification_records
                   (timestamp, img_name, pred_class, confidence)
                   VALUES (?, ?, ?, ?)
    """, (timestamp, img_name, pred_class, confidence)
    )

    conn.commit()
    conn.close()

def fetch_all():
    conn = get_db_conn()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM classification_records")
    rows = cursor.fetchall()

    conn.close()
    return rows
