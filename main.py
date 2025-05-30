from preprocess import (
    csv,
    json,
    log
)

csv = csv.CSVPreprocessor(file_path="source/logs_MidFlow_ESB.csv")
json = json.JSONPreprocessor(file_path="source/logs_SecuCheck.json")
log = log.LOGPreprocessor(log_path="source/logs_CoreBank.log")

""" csv.load_data()
csv.view_data()
csv.get_info()
csv.get_description()

json.load_data()
json.view_data() """

log.preprocess()