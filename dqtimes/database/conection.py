from sqlalchemy import create_engine

DATABASE_URL = "postgresql+psycopg2://user:password@localhost:5432/seubanco"

engine = create_engine(DATABASE_URL)
