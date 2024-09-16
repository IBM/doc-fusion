import requests
import re
from langchain_core.documents import Document

class WebCrawler:
    def __init__(self, url: str):
        """
        Takes url as input string, extracts the web content and return the output in string.
        Args:
            url: The url of the web page.
        
        Returns:
            str: The crawled web page.
        """
        
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
        }
        self.url = url

    def clean_text(self, text):
        link_pattern = r"https?://[^\s]+"
        image_pattern = r"\[(Image\s+\d+)|(!\[.+?\]\(.+\))\]\(.+\)"
        clean_text = re.sub(link_pattern, "", text)
        clean_text = re.sub(image_pattern, "", clean_text)
        clean_text = clean_text.replace("[!](", "").replace("!](", "").replace("URL Source:", "").replace("Markdown Content:", "").replace("Title:", "")
        return clean_text
   
    def load(self):
        """
        Takes url as input string, extracts the web content and return the output in string.
        Args:
            url: The url of the web page.
        
        Returns:
            str: The crawled web page.
        """
        try:
            response = requests.get("https://r.jina.ai/" + self.url)
            result = response.text
            if len(result) == 0:
                return result
            result = self.clean_text(result)
            result = [Document(page_content=str(result), metadata={"WebsiteURL": str(self.url)})]
            return {"text": result, "tables": []}
        except Exception as e:
            print(f"Error: {e}")
            return ''