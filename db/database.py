from sqlmodel import create_engine, SQLModel
from sqlalchemy import inspect, text, Table, MetaData
from dotenv import load_dotenv
import os
from sqlalchemy.exc import IntegrityError
from sqlalchemy.dialects.postgresql import insert
import logging
import time

# Configuración de logging mínima
logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.ERROR)

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL no configurada")

# Engine optimizado
engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_size=30,
    max_overflow=50,
    pool_pre_ping=True,
    executemany_mode='values',
    executemany_values_page_size=10000
)

def init_db():
    import models
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

def add_data(data, table_name: str, batch_size: int = 10000):
    """
    Inserción directa ultra rápida usando SQLAlchemy Core
    - table_name: Nombre de la tabla destino
    - batch_size: Tamaño óptimo de lote (10,000 es buen valor)
    - Retorna: Tupla (éxitos, fallos, tiempo)
    """
    if not data:
        return (0, 0, 0.0)
    
    start_time = time.time()
    total = len(data)
    successes = 0
    errors = 0
    
    # Convertir objetos a diccionarios
    dict_list = [d.dict() for d in data]
    
    # Obtener metadatos de la tabla
    metadata = MetaData()
    metadata.reflect(bind=engine)
    table = Table(table_name, metadata, autoload_with=engine)
    
    # Inserción masiva directa
    with engine.begin() as connection:
        try:
            # Intento de inserción masiva
            connection.execute(table.insert(), dict_list)
            successes = total
        except Exception as mass_error:
            # Fallback: Inserción por lotes
            for i in range(0, total, batch_size):
                batch = dict_list[i:i + batch_size]
                try:
                    connection.execute(table.insert(), batch)
                    successes += len(batch)
                except IntegrityError:
                    # Fallback: Inserción individual
                    for item in batch:
                        try:
                            connection.execute(table.insert(), item)
                            successes += 1
                        except Exception:
                            errors += 1
                except Exception:
                    errors += len(batch)
    
    elapsed = time.time() - start_time
    rate = successes / elapsed if elapsed > 0 else 0
    
    print(f"🚀 {successes}/{total} registros insertados en {elapsed:.2f}s "
          f"({rate:.0f} reg/s) | Errores: {errors}")
    
    return (successes, errors, elapsed)

def get_table_names():
    inspector = inspect(engine)
    return inspector.get_table_names()

if __name__ == "__main__":
    init_db()
    print("DB inicializada | Tablas:", get_table_names())