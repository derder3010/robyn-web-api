import os
from sqlalchemy import create_engine, text

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
print(DATABASE_URL)
if DATABASE_URL:
    engine = create_engine(DATABASE_URL)
    conn = engine.connect()

    res = conn.execute(text("SELECT now()")).fetchall()
    print(res)
