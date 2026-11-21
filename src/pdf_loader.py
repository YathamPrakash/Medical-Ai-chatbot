from pypdf import PdfReader
from langchain_core.documents import Document


def load_pdf(file_path:str)->list[Document]:
 documents:list[Document]=[]
 reader=PdfReader(file_path)
 pages=reader.pages
 for i,page in enumerate(pages):
  text=page.extract_text().strip() or " "
  if(text):
   documents.append(Document(page_content=text, metadata={"page": i + 1}))
  else:
   raise ValueError(f"Failed to extract data from Page {i+1}")
 return documents

 
  
    
