import os
from langchain_core.prompts import ChatPromptTemplate
from src.retrieval import get_relevant_docs
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from  src.llm import llm
from src.embedding import get_hf_embeddings
from dotenv import load_dotenv
load_dotenv()

prompt = ChatPromptTemplate.from_template("""
    You are an AI medical assistant.

    Your task is to provide accurate and helpful medical information
    using only the provided context.

    If the answer is not available in the provided context,
    respond: "I'm sorry, we don't have that information."

    Context:
    {context}

    Question:
    {question}

    Answer:
    """
            )

def format_answer_docs(docs):
    return "\n".join(doc.page_content for doc in docs)

chain=(
    {
        "context":RunnableLambda(
            lambda input:format_answer_docs(get_relevant_docs(
                index_name=os.getenv("PINECONE_INDEX_NAME"),
                embedding_model=get_hf_embeddings(
                    modelname="sentence-transformers/all-MiniLM-L6-v2"
                ),
                query=input["question"]
            ))
        ),
        "question":RunnableLambda(
            lambda input: input["question"]
        )
    }
    |prompt
    |llm
    |StrOutputParser(strip=True)  
)

def generate_answer(question):
    if not question:
        raise ValueError("Question cannot be empty.")   
    return chain.invoke({"question": question})






