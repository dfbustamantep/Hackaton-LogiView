from sqlmodel import SQLModel, Field, Relationship
from enum import Enum
from datetime import datetime
from typing import (
    List,
    Optional
)

class Operation(str, Enum):
    TRANSFER = "TRANSFERIR"
    CONSIGN = "CONSIGNAR"
    WITHDRAW= "RETIRAR"
    
class Account(str, Enum):
    SAVINGS = "AHORROS"
    CHECKING = "CORRIENTE"    

class ApplicationType(str, Enum):
    SECUCHECK = "SecuCheck"
    MIDFLOWESB = "Midflow_ESB"
    COREBANK = "CoreBank"
    
class ValidateResult(str, Enum):
    APROVED = "APROBADA"
    REJECTED = "RECHAZADA"

class LogLevel(str, Enum):
    INFO = "INFO"
    ERROR= "ERROR"

class Direction(str, Enum):
    REQUEST = "REQUEST"
    RESPONSE = "RESPONSE"
    
class StatusCode(int, Enum):
    OK = 200
    INTERNAL_SERVER_ERROR = 500

class ApplicationTransaction(SQLModel, table=True):
    transaction_id: Optional[str] = Field(
        default=None,
        foreign_key="transaction.transaction_id",
        primary_key=True,
        nullable=False
    )
    
    application_name: ApplicationType = Field(
        default=None,
        foreign_key="application.name",
        primary_key=True
    )
    
    state: Optional[str] = Field(
        sa_column_kwargs={"nullable": True}
    )
    timestamp: datetime = Field(
        sa_column_kwargs={"nullable": False}
    )
    validate_result: Optional[ValidateResult] = Field(
        sa_column_kwargs={"nullable": True}
    )
    failed_reason: Optional[str] = Field(
        default=None
    )
    account_type: Optional[Account] = Field(
        sa_column_kwargs={"nullable": True}
    )
    log_level: Optional[LogLevel] = Field(
        sa_column_kwargs={"nullable": True}
    )
    operation: Optional[Operation] = Field(
        sa_column_kwargs={"nullable": True}
    )
    direction: Optional[Direction] = Field(
        sa_column_kwargs={"nullable": True}
    )
    status_code: Optional[StatusCode] = Field(
        sa_column_kwargs={"nullable": True}
    )
    amount: Optional[float] = Field(
        sa_column_kwargs={"nullable": True}
    )
    transaction_type: Optional[str] = Field(
        sa_column_kwargs={"nullable": True}
    )
    realized_verifications: Optional[str] = Field(
        sa_column_kwargs={"nullable": True}
    )
    latency: Optional[str] = Field(
        sa_column_kwargs={"nullable": True}
    )
    
class Transaction(SQLModel, table=True):
    transaction_id: str = Field(primary_key=True, index=True)
    user_id: str = Field(nullable=False)
    module: str = Field(sa_column_kwargs={"nullable": False})
    ip_address: str = Field(sa_column_kwargs={"nullable": False})
    
    applications: List["Application"] = Relationship(
        back_populates="transactions",
        link_model=ApplicationTransaction
    )
    
class Application(SQLModel, table=True):
    name: ApplicationType = Field(primary_key=True, index=True)
    
    transactions: List[Transaction] = Relationship(
        back_populates="applications",
        link_model=ApplicationTransaction
    )
    
    