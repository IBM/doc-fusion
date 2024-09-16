import pandas as pd
from langchain.docstore.document import Document

class StructuredLoader:
    def __init__(self, file_path: str):
        """
        Initialize the StructuredLoader with the path to the file.

        Args:
        file_path (str): Path to the Excel or CSV file.
        """
        self.file_path = file_path
        self.file_type = file_path.split('.')[1]

    def read_file(self) -> pd.DataFrame:
        """
        Read the file into a pandas DataFrame.

        Returns:
        pd.DataFrame: DataFrame containing the file contents.
        """
        if self.file_type == 'csv':
            return pd.read_csv(self.file_path)
        elif self.file_type == 'xlsx':
            return pd.read_excel(self.file_path)
        else:
            raise ValueError("Unsupported file type. Please use 'csv' or 'excel'.")

    def load(self):
        """
        Parse dataframe to Document

        Returns:
        List of Documents
        """
                
        if self.file_type == 'csv':
            df = pd.read_csv(self.file_path)
        elif self.file_type == 'xlsx':
            df = pd.read_excel(self.file_path)
        else:
            raise ValueError("Unsupported file type")

        documents = []
        for _, row in df.iterrows():
            # Trim whitespace from each cell value
            content = ' | '.join(str(value).strip() for value in row.values)
            json_data = {key: str(value).strip() for key, value in row.items()}
            file_path_components = self.file_path.split('/')
            file_name = file_path_components[-1].rsplit('.', 1)
            metadata={"json_format":json_data,"source":file_name[0],"page":"Sheet1","table":1,"row":1}

            documents.append(Document(page_content=content, metadata=metadata))

        return {"text": [],"tables": [documents]}
