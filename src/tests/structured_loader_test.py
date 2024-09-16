import unittest
import pandas as pd
from langchain.docstore.document import Document
from src.core.structured_data_loader import StructuredLoader

class TestStructuredLoader(unittest.TestCase):

    def test_read_csv(self):
        loader = StructuredLoader('src/tests/test-files/samplestructured2.csv')
        df = loader.read_file()
        expected_df = pd.read_csv('src/tests/test-files/samplestructured2.csv')
        pd.testing.assert_frame_equal(df, expected_df)

    def test_read_excel(self):
        loader = StructuredLoader('src/tests/test-files/samplestructured1.xlsx')
        df = loader.read_file()
        expected_df = pd.read_excel('src/tests/test-files/samplestructured1.xlsx')
        pd.testing.assert_frame_equal(df, expected_df)

    def test_load_csv(self):
        loader = StructuredLoader('src/tests/test-files/samplestructured2.csv')
        documents = loader.load()
        
        expected_documents = [
            Document(page_content="Alice | 30 | New York", metadata={'name': 'Alice', 'age': '30', 'city': 'New York'}),
            Document(page_content="Bob | 25 | Los Angeles", metadata={'name': 'Bob', 'age': '25', 'city': 'Los Angeles'}),
            Document(page_content="Carol | 35 | Chicago", metadata={'name': 'Carol', 'age': '35', 'city': 'Chicago'})
        ]
        
        self.assertEqual(len(documents), len(expected_documents))
        for doc, expected_doc in zip(documents, expected_documents):
            self.assertEqual(doc.page_content, expected_doc.page_content)
            self.assertEqual(doc.metadata, expected_doc.metadata)
    
    def test_load_excel(self):
        loader = StructuredLoader('src/tests/test-files/samplestructured1.xlsx')
        documents = loader.load()
        
        expected_documents = [
            Document(page_content="Alice | 30 | New York", metadata={'name': 'Alice', 'age': '30', 'city': 'New York'}),
            Document(page_content="Bob | 25 | Los Angeles", metadata={'name': 'Bob', 'age': '25', 'city': 'Los Angeles'}),
            Document(page_content="Carol | 35 | Chicago", metadata={'name': 'Carol', 'age': '35', 'city': 'Chicago'})
        ]
        
        self.assertEqual(len(documents), len(expected_documents))
        for doc, expected_doc in zip(documents, expected_documents):
            self.assertEqual(doc.page_content, expected_doc.page_content)
            self.assertEqual(doc.metadata, expected_doc.metadata)

    # def test_invalid_file_type(self):
    #     loader = StructuredLoader('src/tests/test-files/samplestructured2.csv')
    #     with self.assertRaises(ValueError):
    #         loader.read_file()

if __name__ == '__main__':
    unittest.main()
