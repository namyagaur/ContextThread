from src.document import Document
import os

def load_text_file(file_path):
    with open(file_path,"r") as file:
        content = file.read()
    
    filename = os.path.basename(file_path)
    d = Document(
        id = filename,
        title=filename,
        content=content,
        source=file_path,
        date="unknown"
    )
    return d
