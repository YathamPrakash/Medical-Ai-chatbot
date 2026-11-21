from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def  split_chunks(documnets:list[Document])->list[Document]:
    splitter=RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks=splitter.split_documents(documnets)
    if(chunks):
        return chunks
    raise ValueError("No chunks were created from the documents.")
