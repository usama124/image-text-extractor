import nltk
import pandas as pd
from unstructured.documents.html import HTMLDocument
from xlsx2html import xlsx2html

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


def excel_to_csv(file_path: str):
    read_file = pd.read_excel(file_path)
    # read_file.to_csv('Data/result.csv', index=None, header=True)
    xlsx2html(file_path, 'Data/workbook.html')
    doc = HTMLDocument.from_file("Data/workbook.html")
    return doc.pages[0]
