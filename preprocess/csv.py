import pandas as pd
import db.models as models
from typing import List, Optional
from datetime import datetime
import numpy as np  # Importar numpy para manejar NaN

class CSVPreprocessor:
    file_path: str
    df: pd.DataFrame
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.transactions: List[models.Transaction] = []
        self.app_transactions: List[models.ApplicationTransaction] = []
    
    def load_data(self) -> None:
        # Leer CSV convirtiendo campos vacíos en NaN
        self.df = pd.read_csv(self.file_path, na_values=['', ' '])
        
    def _parse_int(self, value) -> Optional[int]:
        """Maneja explícitamente valores NaN y cadenas vacías"""
        if pd.isna(value) or value == '':
            return None
        try:
            return int(value)
        except (TypeError, ValueError):
            return None
    
    def preprocess(self) -> None:
        for _, row in self.df.iterrows():
            # Construir transacción genérica
            transaction = models.Transaction(
                transaction_id=str(row['transaction_id']),
                user_id=str(row['user_id']),
                ip_address=str(row['ip_address']),
                module=str(row['modulo'])
            )
            self.transactions.append(transaction)
            
            # Conversión de timestamp
            ts = datetime.strptime(str(row['timestamp']), "%Y-%m-%d %H:%M:%S")
            
            # Parseo de status_code
            status_raw = str(row['status_code'])
            status = (
                models.StatusCode.OK 
                if status_raw == "200" 
                else models.StatusCode.INTERNAL_SERVER_ERROR
            )
            
            # Crear ApplicationTransaction con manejo robusto de latencia
            app_transaction = models.ApplicationTransaction(
                transaction_id=transaction.transaction_id,
                application_name=models.ApplicationType.MIDFLOWESB,
                timestamp=ts,
                log_level=(
                    models.LogLevel.INFO 
                    if str(row['nivel_log']) == 'INFO' 
                    else models.LogLevel.ERROR
                ),
                direction=(
                    models.Direction.REQUEST 
                    if str(row['direction']).lower() == 'request' 
                    else models.Direction.RESPONSE
                ),
                operation=(
                    models.Operation.CONSIGN 
                    if str(row['operation']) == 'consignar' 
                    else models.Operation.WITHDRAW 
                    if str(row['operation']) == 'retirar' 
                    else models.Operation.TRANSFER
                ),
                status_code=status,
                latency=self._parse_int(row['latency_ms']),  # Usar función mejorada
                validate_result=None,
                failed_reason=None,
                realized_verifications=None,
                transaction_type=None,
                account_type=None,
                state=None,
                amount=None
            )
            
            print(app_transaction)
            self.app_transactions.append(app_transaction)

