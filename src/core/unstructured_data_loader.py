import pymupdf
from langchain_core.documents import Document
import itertools
import re
import os
import mammoth
from xhtml2pdf import pisa

class UnstructuredLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.file_type = file_path.split('.')[1]

    def extract_page_content(self,doc_name,page,page_no):
        list_tables=page.find_tables()
        y0=0
        page_text=[]
        page_table=[]

        i=1
        for j in range(len(list_tables.tables)):
            table = list_tables[j]
            df = table.to_pandas() 

            rect = table.bbox
            y1=rect[1]
            new_rect=(0,y0,612,y1)

            page_content=page.get_text("text",clip=new_rect)
            metadata={"source":doc_name,"page":page_no,"index":i}
            i=i+1

            page_text.append(Document(
                page_content=page_content,
                metadata=metadata))
            
            k=1
            if df is not None:
                for _, row in df.iterrows():
                    table_content = ' | '.join(str(value).strip() for value in row.values)
                    json_data = {key: str(value).strip() for key, value in row.items()}
                
                    metadata={"json_format":json_data,"source":doc_name,"page":page_no,"table":j,"row":k}
                    page_table.append(Document(
                        page_content=table_content,
                        metadata=metadata))
                    
                    k=k+1
            
            y0=rect[3]
        
        new_rect=(0,y0,612,792)

        page_content=page.get_text("text",clip=new_rect)
        metadata={"source":doc_name,"page":page_no,"index":i}
        i=i+1

        page_text.append(Document(
                page_content=page_content,
                metadata=metadata))

        return page_text,page_table
    
    def remove_img_tags(self,data):
        p = re.compile(r'<img.*?/>')
        return p.sub('', data)
    
    def convert_to_pdf(self,file_path):
        if file_path.endswith('.docx'):
            with open(file_path, "rb") as docx_file:
                result = mammoth.convert_to_html(docx_file)
            html_string = "<!DOCTYPE html><html>"+result.value+"</html>"
            html_sring = html_string.replace("<table>", "<table border=1 style=font-size:40%>")
            html_sring = self.remove_img_tags(html_sring)
            
            pdf_filename = os.path.splitext(os.path.basename(file_path))[0]+'.pdf'
            pdf_filepath = os.path.join('docs', pdf_filename)
            
            with open(pdf_filepath, "wb") as pdf_file:
                pisa_status = pisa.CreatePDF(html_sring, dest=pdf_file)

            return str(pdf_filepath)
            
        return str(file_path)

    def load(self):
        converted_file=False
        if self.file_type =='docx':
            self.file_path=self.convert_to_pdf(self.file_path)
            self.file_type='pdf'
            converted_file=True
            
        if self.file_type == 'pdf':
            doc=pymupdf.open(self.file_path)
            doc_name=self.file_path
            texts=[]
            tables=[]
            for i in range(len(doc)):
                text,table=self.extract_page_content(doc_name,doc[i],i+1)
                texts.append(text),
                tables.append(table)
                
            final_text_list = list(itertools.chain(*texts))
            if(converted_file):
                os.remove(self.file_path)

            return {"text":final_text_list,"tables":tables}