from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.core.unstructured_data_loader import UnstructuredLoader
import json
from config.app_config import AppConfig
app_config = AppConfig()

class Splitter:
    def __init__(self):
        
        with open(app_config.DATA_CONFIG_PATH, 'r') as configfile:
            self.config = json.loads(configfile.read())
  
        self.chunk=self.config.get('chunk') if 'chunk' in self.config else True
        self.chunk_table_rows=self.config.get('chunk_table_rows') if 'chunk_table_rows' in self.config else True
        self.chunk_table_row_size=self.config.get('chunk_table_row_size') if 'chunk_table_row_size' in self.config else 1
        self.chunk_table_row_overlap=self.config.get('chunk_table_row_overlap') if 'chunk_table_row_overlap' in self.config else 0
        self.chunk_table_output_format=self.config.get('chunk_table_output_format') if 'chunk_table_output_format' in self.config else "json"
        self.chunk_text_size=self.config.get('chunk_text_size') if 'chunk_text_size' in self.config else 512
        self.chunk_text_overlap=self.config.get('chunk_text_overlap') if 'chunk_text_overlap' in self.config else 40

    def split_tables(self,tables):
        table_chunks=[]
        
        for table in tables:
            if self.chunk_table_rows is False:
                self.chunk_table_row_size=len(table)

            start = 0
            while start < len(table):

                end = min(start + self.chunk_table_row_size, len(table))
                chunked_table=table[start:end]

                if self.chunk_table_output_format=="json":
                    table_content=""
                    for i in range(len(chunked_table)):
                        table_content+=str(chunked_table[i].metadata['json_format'])

                    metadata={"source":chunked_table[0].metadata['source'],"page":chunked_table[0].metadata['page'],"table":chunked_table[0].metadata["table"],"rows_start":start+1,"rows_end":end}
                    table_chunks.append(Document(page_content=table_content,metadata=metadata))

                elif self.chunk_table_output_format=="md":
                    columns=chunked_table[0].metadata['json_format'].keys()
                    md_header = ' | '.join(columns)
                    md_separator = ' | '.join(['---'] * len(columns))
                    md_table_header = f"{md_header}\n{md_separator}\n"
                    table_content=md_table_header
                    for i in range(len(chunked_table)):
                        table_content+=str(chunked_table[i].page_content)
                        table_content+="\n"

                    metadata={"source":chunked_table[0].metadata['source'],"page":chunked_table[0].metadata['page'],"table":chunked_table[0].metadata["table"],"rows_start":start+1,"rows_end":end}
                    table_chunks.append(Document(page_content=table_content,metadata=metadata))

                start += self.chunk_table_row_size - self.chunk_table_row_overlap
                

        return table_chunks

    def split_text(self,documents):
        character_splitter = RecursiveCharacterTextSplitter(
            separators=["\n\n", "\n", ". ", " ", ""],
            chunk_size=self.chunk_text_size,
            chunk_overlap=self.chunk_text_overlap
        )
        
        chunked_documents = []
        for doc in documents:
            chunks = character_splitter.split_text(doc.page_content)

            for chunk in chunks:
                chunked_documents.append(Document(metadata=doc.metadata, page_content=chunk))

        return chunked_documents
    
    def split(self,documents):
        text = []
        tables = []
        if(self.chunk):
            if documents['text'] != []:
                text=self.split_text(documents['text'])
        else:
            text=documents['text']

        if documents['tables'] != []:
            tables=self.split_tables(documents['tables'])
        
        return text+tables