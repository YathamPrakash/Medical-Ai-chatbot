import re
from langchain_core.documents import Document

def clean_documnets(documents:list[Document])->list[Document]:
    cleaned_documents:list[Document]=[]
    for doc in documents:
        text=doc.page_content.strip()
        if text:
            text=text.replace("\r\n","\n").replace("\r","\n")
            text=re.sub(r"[\t]"," ",text)
            text=re.sub(r"\n{2,}","\n",text)
            text=re.sub(r" +"," ",text)
            text=text.strip()
            cleaned_documents.append(Document(page_content=text,metadata=doc.metadata.copy()))
    if not cleaned_documents:
        raise ValueError("No valid documents found after cleaning")
    return cleaned_documents