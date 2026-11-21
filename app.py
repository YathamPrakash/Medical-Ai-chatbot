
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from upload_flow import save_uploaded_pdf, process_pdf
from rag_pipeline import generate_answer


st.set_page_config(
    page_title="Medical RAG Assistant",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Medical RAG Assistant")

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "document_ready" not in st.session_state:
    st.session_state.document_ready = False


# --------------------------------
# DOCUMENT UPLOAD
# --------------------------------

st.sidebar.header("Upload Medical Document")

uploaded_file = st.sidebar.file_uploader(
    "Select a PDF document",
    type=["pdf"]
)

if uploaded_file is not None:

    st.sidebar.write(f"Selected: {uploaded_file.name}")

    if st.sidebar.button("Upload Document"):

        try:
            with st.spinner("Saving document..."):

                saved_path = save_uploaded_pdf(uploaded_file)

            st.sidebar.success(
                f"Document saved: {saved_path.name}"
            )

            with st.spinner("Processing document..."):

                result = process_pdf(saved_path)

            st.session_state.document_ready = True

            st.sidebar.success("Document processed successfully!")

            st.sidebar.write(f"Pages: {result['total_pages']}")
            st.sidebar.write(f"Chunks: {result['total_chunks']}")

        except Exception as error:
            st.sidebar.error(f"Upload failed: {error}")


# --------------------------------
# CHAT INTERFACE
# --------------------------------

st.header("Chat with your medical document")

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


question = st.chat_input(
    "Ask a medical question..."
)

if question:

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        with st.spinner("Generating answer..."):

            try:
                answer = generate_answer(question)
                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as error:
                st.error(f"Error: {error}")
