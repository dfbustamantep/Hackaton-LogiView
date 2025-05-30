from sqlmodel import SQLModel, Field
from enum import Enum

class Type(str, Enum):
    TRANSFER = "transferir",
    CONSIGN = "consignar",
    WITHDRAW = "retirar"
    
class Account(str, Enum):
    SAVINGS = "ahorros",
    CHECKING = "corriente"    
    
class ApplicationType(str, Enum):
    SECUCHECK = "SecuCheck",
    MIDFLOWESB = "Midflow_ESB",
    COREBANK = "CoreBank"
    
class Transaction(SQLModel, table=True):
    name: str = Field(primary_key=True, index=True)
    user_id: str = Field(primary_key=True, index=True, nullable=False)
    amount: float = Field(sa_column_kwargs={"nullable": False})
    module: str = Field(sa_column_kwargs={"nullable": False})
    ip_address: str = Field(sa_column_kwargs={"nullable": False})
    
class Application(SQLModel, table=True):
    name: ApplicationType = Field(primary_key=True, index=True)