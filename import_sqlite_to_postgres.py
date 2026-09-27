import sqlite3
import psycopg2

# ---------- SQLite ----------
sqlite_conn = sqlite3.connect("jobs_2023.sqlite")
sqlite_cursor = sqlite_conn.cursor()

# ---------- PostgreSQL ----------
pg_conn = psycopg2.connect(
    host="localhost",
    database="sql_course",
    user="postgres",
    password="Postgres@123"
)

pg_cursor = pg_conn.cursor()

print("Connected to both databases!")

# Tables to import
tables = [
    "company_dim",
    "job_postings_fact",
    "skills_dim",
    "skills_job_dim"
]

for table in tables:
    print(f"Importing {table}...")

    sqlite_cursor.execute(f"SELECT * FROM {table}")
    rows = sqlite_cursor.fetchall()

    # Get column names
    sqlite_cursor.execute(f"PRAGMA table_info({table})")
    columns = [column[1] for column in sqlite_cursor.fetchall()]

    column_names = ", ".join(columns)
    placeholders = ", ".join(["%s"] * len(columns))

    # Create PostgreSQL table
    pg_cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table} (
            {", ".join(f'"{column}" TEXT' for column in columns)}
        )
    """)

    # Insert data
    insert_query = f"""
        INSERT INTO {table} ({column_names})
        VALUES ({placeholders})
    """

    pg_cursor.executemany(insert_query, rows)

    print(f"{len(rows)} rows imported into {table}")

pg_conn.commit()

print("ALL DATA IMPORTED SUCCESSFULLY!")

sqlite_conn.close()
pg_conn.close()
# Testing GitHub connections
# GitHub test
