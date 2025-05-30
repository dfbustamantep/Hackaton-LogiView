from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy import inspect, text
from dotenv import load_dotenv
import os

# Carga las variables del archivo .env
load_dotenv()

# URL de la base de datos desde las variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL environment variable is not set.")

# Crea el engine (asegúrate que nunca quede None)
engine = create_engine(DATABASE_URL, echo=True)


def init_db():
    import models  # importa aquí para que SQLModel registre las tablas
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


def list_tables_inspector() -> list[str]:
    """Devuelve los nombres de las tablas usando SQLAlchemy Inspector."""
    inspector = inspect(engine)
    return inspector.get_table_names()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.\n")

    print("Tablas (Inspector):", list_tables_inspector())
