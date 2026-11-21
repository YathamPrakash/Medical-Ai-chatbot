from src.vector_store import create_pinecone_vector


def get_relevant_docs(index_name:str, embedding_model, query:str):

    if  query.strip() == "":
        print("Query is empty.")
        return []
    else:
        vector_store=create_pinecone_vector(index_name, embedding_model)
        relevant_retrieved_docs = vector_store.similarity_search(query, k=5)
        return relevant_retrieved_docs


