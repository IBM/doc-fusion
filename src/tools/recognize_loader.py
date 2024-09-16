from langchain.agents import tool
import time

@tool("recognize_loader")
def recognize_loader(Format:str) -> str:
    """
    Takes format as input and returns the relevant loader.

    Args:
        Format: The format of the file that needs to be sourced. Format can be PDF, DOCX, CSV, TXT, XLSX and URL.
    
    Returns:
        str: The relevant function name. 
    """
    start_time = time.time()
    Format = Format.strip().lower()
    loader = None

    if "pdf" in Format or "docx" in Format or "txt" in Format or "md" in Format:
        loader = "UnstructuredLoader"
    elif "csv" in Format or "xlsx" in Format:
        loader = "StructuredLoader"
    elif "url" in Format:
        loader = "WebCrawler"

    end_time = time.time()
    execution_time = end_time - start_time
    return loader