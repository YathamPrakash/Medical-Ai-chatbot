from pinecone import Pinecone,ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os
load_dotenv()

pinecone = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

def create_pinecone_index(index_name, embedding_model):
    checkIndex=pinecone.has_index(index_name)
    if not checkIndex:
         pinecone.create_index(
            name=index_name,
            dimension=len(embedding_model.embed_query("Hello world")),
            metric="cosine",
            spec=ServerlessSpec(
                cloud=os.getenv("PINECONE_CLOUD"),
                region=os.getenv("PINECONE_REGION")
            )
        )
         print(f"Created index: {index_name}")
    else:
        print(f"Index already exists: {index_name}")

    return pinecone.Index(index_name)

def create_pinecone_vector(index_name, embedding_model):
    index=create_pinecone_index(index_name, embedding_model)
    vector_store = PineconeVectorStore(
        index=index,
        embedding=embedding_model
    )
    return vector_store

def chunks_store_to_pinecone(index_name, embedding_model, chunks):
    if not chunks:
        print("No chunks to add to Pinecone.")
        return {
            "message": "No chunks to add to Pinecone.",
            "ids": []
        }
    else:
        vector_store = create_pinecone_vector(index_name, embedding_model)
        id = vector_store.add_documents(chunks)
        print(f"Added {len(chunks)} chunks to Pinecone with IDs: {id}")
        return {
            "message": f"added the {len(chunks)} chunks to Pinecone",
            "ids": id
        }


# def get_similarity_search(index_name, embedding_model,question):
#     vector_store = create_pinecone_vector(index_name, embedding_model)
#     response=vector_store.similarity_search(question, k=5)
#     return response
    

