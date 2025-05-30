import pandas as pd
import db.models as models
from typing import List
from datetime import datetime

class CSVPreprocessor:
    file_path: str
    df: pd.DataFrame
    transactions: List[models.Transaction] = []
    app_transactions: List[models.ApplicationTransaction] = []
    latencies: List[tuple] = []
    
    def __init__(self, file_path):
        self.file_path = file_path
    
    def load_data(self):
        self.df = pd.read_csv(self.file_path)
        
    def preprocess(self):
        for index, row in self.df.iterrows():
            transaction = models.Transaction(
                transaction_id=str(row.get('transaction_id')),
                user_id=str(row.get('user_id')),
                ip_address=str(row.get('ip_address')),
                module=str(row.get('modulo'))
            )
            self.transactions.append(transaction)
            
            raw_latency = row.get('latency_ms')
            latency_str = str(raw_latency) if pd.notnull(raw_latency) else ""
            self.latencies.append((transaction.transaction_id, latency_str))
            
            app_transaction = models.ApplicationTransaction(
                transaction_id=str(row.get('transaction_id')),
                application_name=models.ApplicationType.MIDFLOWESB,
                timestamp= datetime.strptime(str(row.get('timestamp')),  "%Y-%m-%d %H:%M:%S"),
                log_level=models.LogLevel.INFO if str(row.get('nivel_log')) == 'INFO' else models.LogLevel.ERROR,
                direction=models.Direction.REQUEST if str(row.get('direction')) == 'request' else models.Direction.RESPONSE,
                operation=models.Operation.CONSIGN if str(row.get('operation')) == 'consignar' else models.Operation.WITHDRAW if str(row.get('operation')) == 'retirar' else models.Operation.TRANSFER,
                status_code=models.StatusCode.OK if str(row.get('transaction_id')) == '200' else models.StatusCode.INTERNAL_SERVER_ERROR,
                latency=str(row.get('latency_ms')) if not pd.isnull(row.get('latency_ms')) else "NaN",
                validate_result=None,
                failed_reason=None,
                realized_verifications=None,
                transaction_type=None,
                account_type=None,
                state=None,
                amount=None
            )
            
            self.app_transactions.append(app_transaction)