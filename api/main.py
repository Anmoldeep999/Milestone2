import os
import socket
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector

DB_HOST = os.getenv("DB_HOST", "mariadb")
DB_USER = os.getenv("DB_USER", "milestone_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "secretpassword")
DB_NAME = os.getenv("DB_NAME", "milestone_db")

app = FastAPI()

# CORS zodat browser vanaf frontend (andere port) mag callen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # voor opdracht: mag simpel
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
    )


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    # Tabel met één naam
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS names (
            id INT PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        )
        """
    )
    # Kijk of er al een rij is
    cur.execute("SELECT COUNT(*) FROM names")
    (count,) = cur.fetchone()
    if count == 0:
        # Zet hier je eigen naam
        cur.execute(
            "INSERT INTO names (id, name) VALUES (%s, %s)",
            (1, "Anmoldeep Singh"),
        )
    conn.commit()
    cur.close()
    conn.close()


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/user")
def get_user():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name FROM names WHERE id = 1")
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return {"name": row[0]}
    return {"name": "Unknown"}


@app.get("/container")
def get_container():
    pod_name = socket.gethostname()
    custom_id = f"AS-{pod_name}"
    return {"container_id": custom_id}


@app.get("/health")
def health():
    return {"status": "ok"}
