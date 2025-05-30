from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy import inspect, text
from dotenv import load_dotenv
import os
from sqlalchemy.exc import IntegrityError
from db import models

# Carga las variables del archivo .env
load_dotenv()

# URL de la base de datos desde las variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL environment variable is not set.")

# Crea el engine (asegúrate que nunca quede None)
engine = create_engine(DATABASE_URL, echo=True)


def init_db():
    import models
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

def add_data(data):
    with Session(engine) as session:
        for item in data:
            try:
                session.add(item)
                session.commit()
            except IntegrityError as e:
                session.rollback()
                print(f"[WARNING] Error al insertar {item}: {e.orig}")

def get_session():
    with Session(engine) as session:
        yield session
        


def list_tables_inspector() -> list[str]:
    """Devuelve los nombres de las tablas usando SQLAlchemy Inspector."""
    inspector = inspect(engine)
    return inspector.get_table_names()

def update_latencies(latencies):
        """
        Ejecuta un UPDATE por cada transaction_id para asignar la latencia
        previamente extraída.
        """
        with Session(engine) as session:
            for tx_id, latency_str in latencies:
                session.query(models.ApplicationTransaction) \
                    .filter_by(transaction_id=tx_id) \
                    .update({"latency": latency_str})
            session.commit()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.\n")

    print("Tablas (Inspector):", list_tables_inspector())
