from preprocess import (
    csv,
    json,
    log
)

from db.database import add_data


csv = csv.CSVPreprocessor(file_path="source/logs_MidFlow_ESB.csv")
json = json.JSONPreprocessor(file_path="source/logs_SecuCheck.json")
log = log.LOGPreprocessor(log_path="source/logs_CoreBank.log")

csv.load_data()
csv.preprocess()

# json.load_data()
# json.process()

# log.preprocess()
# add_data(log.transactions)
# add_data(log.app_transactions)
# add_data(json.transactions)
# add_data(json.app_transactions)
# add_data(csv.transactions)
