from langchain_huggingface import HuggingFaceEmbeddings


model_kwargs = {"device": "cpu"}
encode_kwargs = {"normalize_embeddings": False}
def get_hf_embeddings(modelname):
    return HuggingFaceEmbeddings(
        model_name=modelname,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs,
    )   

    




