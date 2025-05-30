import db.models as models
from typing import List
from datetime import datetime

class LOGPreprocessor:
    log_path: str
    transactions: List[models.Transaction] = []
    app_transactions: List[models.ApplicationTransaction] = []
    def __init__(self, log_path):
        self.log_path = log_path

    def preprocess(self):
        with open(self.log_path, 'r') as file:
            lines = file.readlines()
        for i, line in enumerate(lines):
            splitted_line = line.split()
            user_id, ip_address = splitted_line[4].split('@')
            transaction_id = splitted_line[8].replace(',', '')
            transaction = models.Transaction(
                transaction_id=transaction_id,
                user_id=user_id,
                module=splitted_line[3].replace('[', '').replace(']', ''),
                ip_address=ip_address
            )
            self.transactions.append(transaction)
            
            format = "%Y-%m-%d %H:%M:%S"
            
            app_transaction = models.ApplicationTransaction(
                transaction_id=transaction_id,
                application_name=models.ApplicationType.COREBANK,
                timestamp=datetime.strptime(splitted_line[0]+ ' ' + splitted_line[1], format),
                amount= float(splitted_line[16].replace(')', '')),
                log_level=models.LogLevel[splitted_line[2].upper()],
                transaction_type=splitted_line[10].upper().replace(',', ''),
                account_type= models.Account.SAVINGS if splitted_line[12] == 'ahorros' else models.Account.CHECKING,
                state=splitted_line[14].replace(',', ''),
                direction=None,
                operation=None,
                status_code=None,
                validate_result=None,
                failed_reason=None,
                realized_verifications=None,
                latency=None,
            )
            self.app_transactions.append(app_transaction)
            