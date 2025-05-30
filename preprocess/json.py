import json 
import db.models as models
from typing import List
from datetime import datetime
format = "%Y-%m-%d %H:%M:%S"

class JSONPreprocessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None
        self.transactions: List[models.Transaction] = []
        self.app_transactions: List[models.ApplicationTransaction] = []

    def load_data(self):
        """Load data from a JSON file."""
        with open(self.file_path, 'r') as file:
            self.data = json.load(file)
        
    def preprocess(self):
        """Process the loaded JSON data into transactions."""
        if not self.data:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        for entry in self.data:
            transaction = models.Transaction(
                transaction_id=entry.get('transaction_id'),
                user_id=entry.get('user_id'),
                ip_address=entry.get('ip_address'),
                module=entry.get('m\u00f3dulo')
            )
            self.transactions.append(transaction)
            
            app_transaction = models.ApplicationTransaction(
                transaction_id=entry.get('transaction_id'),
                application_name=models.ApplicationType.SECUCHECK,
                timestamp=datetime.strptime(entry.get('timestamp'), format),
                validate_result=models.ValidateResult.APROVED if entry.get('resultado_validaci\u00f3n') == 'Aprobada' else models.ValidateResult.REJECTED,
                failed_reason=entry.get('motivo_fallo'),
                realized_verifications=','.join(entry.get('verificaciones_realizadas') if entry.get('verificaciones_realizadas') else []),
                amount= None,
                log_level= None,
                transaction_type= None,
                account_type= None,
                state= None,
                direction=None,
                operation=None,
                status_code=None,
                latency=None,
            )
            
            self.app_transactions.append(app_transaction)