import pandas as pd

class CSVPreprocessor:
    file_path: str
    df: pd.DataFrame
    

    def __init__ (self, file_path):
        self.file_path = file_path
    
    def load_data(self):
        self.df = pd.read_csv(self.file_path) 
        print(f"Data loaded from {self.file_path} with shape {self.df.shape}")

    def view_data(self):
        if self.df is not None:
            print(self.df.head())
        else:
            raise ValueError("DataFrame is not loaded. Please load the data first.")
    
    def get_info(self):
        if self.df is not None:
            return self.df.info()
        else:
            raise ValueError("DataFrame is not loaded. Please load the data first.")
        
    def get_description(self):
        if self.df is not None:
            print(self.df.describe())
        else:
            raise ValueError("DataFrame is not loaded. Please load the data first.")