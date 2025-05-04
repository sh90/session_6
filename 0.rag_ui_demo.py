# pip install streamlit tiktoken openai langchain-community

import os
import streamlit as st
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.schema import Document
import data_info  # Contains your OpenAI key as data_info.open_ai_key
from langchain.document_loaders import TextLoader, PyPDFLoader, UnstructuredWordDocumentLoader
# --------- Config ---------
TEXT_FILE_PATH = "data/onboarding.txt"
CHROMA_PERSIST_DIR = "chroma_store_openai_v2"

LLM_MODEL = "gpt-4o-mini"  # or "gpt-4"
EMBED_MODEL = "text-embedding-3-small"
OPENAI_API_KEY = data_info.open_ai_key
DATA_DIR = "data"
# --------- Load & Split Text ---------
@st.cache_resource
def load_documents():
        documents = []
        for filename in os.listdir(DATA_DIR):
            file_path = os.path.join(DATA_DIR, filename)
            print(file_path)
            if filename.endswith(".txt"):
                loader = TextLoader(file_path)
            elif filename.endswith(".pdf"):
                loader = PyPDFLoader(file_path)
            elif filename.endswith(".docx"):
                loader = UnstructuredWordDocumentLoader(file_path)
            else:
                print(f"[WARN] Skipping unsupported file type: {filename}")
                continue
            docs = loader.load()
            documents.extend(docs)
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        return splitter.split_documents(documents)


# --------- Setup Vector Store ---------
@st.cache_resource
def setup_vectorstore(_docs):
    embedding_model = OpenAIEmbeddings(model=EMBED_MODEL, openai_api_key=OPENAI_API_KEY)
    if os.path.exists(CHROMA_PERSIST_DIR):
        vectordb = Chroma(persist_directory=CHROMA_PERSIST_DIR, embedding_function=embedding_model)
    else:
        vectordb = Chroma.from_documents(_docs, embedding_model, persist_directory=CHROMA_PERSIST_DIR)
        vectordb.persist()
    return vectordb

# --------- Load LLM & QA Chain ---------
@st.cache_resource
def setup_qa_chain(_vectordb):
    llm = ChatOpenAI(model_name=LLM_MODEL, temperature=0, openai_api_key=OPENAI_API_KEY)
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=_vectordb.as_retriever(),
        return_source_documents=True
    )
    return qa_chain

# --------- Streamlit UI ---------
def main():
    st.title("📄 AI Chat - Ask About Your Document")
    st.markdown("Ask questions based **only on the content** in the uploaded document.")

    docs = load_documents()
    vectordb = setup_vectorstore(docs)
    qa_chain = setup_qa_chain(vectordb)

    # Store chat history in session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.text_input("🔍 Ask a question based on the document:")

    if user_input:
        result = qa_chain(user_input)
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("AI", result["result"]))

    # Display chat history
    for sender, msg in st.session_state.chat_history:
        if sender == "You":
            st.markdown(f"**🧑 You:** {msg}")
        else:
            st.markdown(f"**🤖 AI:** {msg}")

if __name__ == "__main__":
    main()
