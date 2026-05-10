from fastapi import Request
import psycopg2
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

db_pool = None

async def init_db_pool():
    db_pool = await asyncpg.create_pool(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        min_size=2,
        max_size=10,
    )

#TODO: Change the data source name to accomodate cloud
async def create_pool():
    return await asyncpg.create_pool(dsn="postgresql://user:password@localhost:5432/")

def get_db_pool(request: Request):
    return request.app.state.db_pool