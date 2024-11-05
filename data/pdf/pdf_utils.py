from config import zh, dim, pdf_loc
import fitz
import re

def get_pdf_raw_blocks(pdf_name):
    pages_blocks = []
    pattern = re.compile(r'[\n\x0f ]')  # Regex pattern to match newline, \x0f, and space characters
    
    with fitz.open(pdf_loc(pdf_name)) as doc:
        for page in doc:
            blocks = [pattern.sub("", block[4]) for block in page.get_text("blocks")]
            page_text = "".join(blocks)
            pages_blocks.append(page_text)
            
    return pages_blocks