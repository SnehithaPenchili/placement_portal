import sqlite3

def get_db_connection():
    conn = sqlite3.connect(
        "placement.db",
        timeout=30,                 #
        check_same_thread=False     # 
    )
    conn.row_factory = sqlite3.Row

    conn.execute("PRAGMA journal_mode=WAL;")   #  allows concurrent reads/writes
    conn.execute("PRAGMA synchronous=NORMAL;")

    return conn