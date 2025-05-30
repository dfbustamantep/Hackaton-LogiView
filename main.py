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
    
    add_data(json.transactions)
    add_data(csv.transactions)
    add_data(log.transactions)
    
    add_data(json.app_transactions)
    add_data(csv.app_transactions)
    add_data(log.app_transactions)
    
if __name__ == "__main__":
    main()
# 