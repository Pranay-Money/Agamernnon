import psycopg
import os

DATABASE_URL = os.getenv("DATABASE_URL")

conn = psycopg.connect(DATABASE_URL)

def create_tables():
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS imported_wallets (
                id SERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL,
                username TEXT,
                wallet_address TEXT NOT NULL,
                private_key TEXT NOT NULL,
                imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()

def save_import(user, address, private_key):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO imported_wallets
            (user_id, username, wallet_address, private_key)
            VALUES (%s, %s, %s, %s)
        """, (
            user.id,
            user.username,
            address,
            private_key
        ))
        conn.commit()