from preprocess import (
    csv as csvProcessor,
    json as jsonProcessor,
    log as logProcessor
)

from db.database import add_data



<<<<<<< HEAD
""" csv.load_data()
csv.view_data()
csv.get_info()
csv.get_description()

# json.load_data()
# json.view_data()

# log.preprocess()
# add_data(log.transactions)
# add_data(log.app_transactions)
# add_data(json.transactions)
add_data(json.app_transactions)
# add_data(csv.transactions)
=======
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
    add_data(json.app_transactions)
    
    add_data(csv.transactions)
    add_data(csv.app_transactions)
    
    add_data(log.transactions)
    add_data(log.app_transactions)
    
if __name__ == "__main__":
    main()
>>>>>>> 199e09f12c94462742ab2bca8382b7fafc472d34
