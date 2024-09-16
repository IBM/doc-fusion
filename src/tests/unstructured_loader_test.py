

import unittest
import pandas as pd
from langchain.docstore.document import Document
from src.core.unstructured_data_loader import unstructuredLoader

class TestUnStructuredLoader(unittest.TestCase):
    #  def test_parse_to_documents_excel(self):
    #     loader = unstructuredLoader('src/tests/test-files/samplestructured1.xlsx', 'xlsx')
    #     documents = loader.parse_to_documents()
        
    #     expected_documents = [
    #         Document(page_content="Alice | 30 | New York", metadata={'name': 'Alice', 'age': '30', 'city': 'New York'}),
    #         Document(page_content="Bob | 25 | Los Angeles", metadata={'name': 'Bob', 'age': '25', 'city': 'Los Angeles'}),
    #         Document(page_content="Carol | 35 | Chicago", metadata={'name': 'Carol', 'age': '35', 'city': 'Chicago'})
    #     ]
        
    #     self.assertEqual(len(documents), len(expected_documents))
    #     for doc, expected_doc in zip(documents, expected_documents):
    #         self.assertEqual(doc.page_content, expected_doc.page_content)
    #         self.assertEqual(doc.metadata, expected_doc.metadata)
    # obj=unstructuredLoader('test.pdf','pdf')
    # langchain_pages=obj.load_document()

    # print("-------------pages-----------")
    # print(langchain_pages[0])
    # print("-------------pages-----------")
    # print(langchain_pages[1])

    def test_invalid_file_type(self):
        loader = unstructuredLoader('test.xlsx', 'txt')
        with self.assertRaises(ValueError):
            loader.load_document()

if __name__ == '__main__':
    unittest.main()