from preprocess import (
    csv as csvProcessor,
    json as jsonProcessor,
    log as logProcessor
)

from db.database import add_data

def main():
    json = jsonProcessor.JSONPreprocessor(file_path="source/logs_SecuCheck.json")
    csv = csvProcessor.CSVPreprocessor(file_path="source/logs_MidFlow_ESB.csv")
    log = logProcessor.LOGPreprocessor(log_path="source/logs_CoreBank.log")
    
    json.load_data()
    csv.load_data()
    
    json.preprocess()
    csv.preprocess()
    log.preprocess()
    
    add_data(data= json.transactions,table_name="transaction")
    add_data(data= csv.transactions,table_name="transaction")
    add_data(data= log.transactions,table_name="transaction")
    
    add_data(data= json.app_transactions, table_name="applicationtransaction")
    add_data(data= csv.app_transactions, table_name="applicationtransaction")
    add_data(data= log.app_transactions, table_name="applicationtransaction")
    
if __name__ == "__main__":
    main()
# 