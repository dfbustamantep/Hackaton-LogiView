import json 

class JSONPreprocessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None

    def load_data(self):
        """Load data from a JSON file."""
        with open(self.file_path, 'r') as file:
            self.data = json.load(file)

    def view_data(self):
        """View the loaded data."""
        if self.data is not None:
            print(json.dumps(self.data, indent=4))
        else:
            print("No data loaded.")
     