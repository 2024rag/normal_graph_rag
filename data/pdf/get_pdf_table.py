import pdfplumber
from config import pdf_loc
import requests
import json
import html2text
from tool import timer
from .pdf_utils import get_pdf_raw_blocks

@timer
def get_pdf_table(pdf_name):
    # url="http://localhost:31500/unstructure"
    # file_path=pdf_loc(pdf_name)
    # form_data={
    #     "extension":".pdf",
    #     "name":f"{pdf_name.split('.')[0]}"
    # }
    # with open(file_path,'rb') as file:
    #     response=requests.post(url,data=form_data,files={"file":file})
    # return [html2text.html2text(item[1])  for item in  json.loads(response.text)]

    def table_to_text(table):
        """
        [[]] ->  str
        """
        str = ""
        for row in table:
            for column in row:
                if column == None:
                    column = ""
                str += f" {column} "
            str += "\n"

        return str


    pdf_table=[]
    with pdfplumber.open(pdf_loc(pdf_name)) as pdf:
        for index,page in enumerate(pdf.pages):
            tables=page.extract_tables()
            if tables==[]:
                continue
            page_txt = get_pdf_raw_blocks(pdf_name)[index]

            for table in tables:
                # pdf_table.append(
                #     {
                #         "table":table_to_text(table),
                #         "page_txt":page_txt
                #     }
                # )
                pdf_table.append(table_to_text(table))

    return pdf_table