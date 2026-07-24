import os
import asyncio

try:
    asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
import time
import streamlit as st
import shutil

from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate

# -------------------------------------------------------
# API KEY
# -------------------------------------------------------

os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

# -------------------------------------------------------
# STREAMLIT UI
# -------------------------------------------------------

st.set_page_config(page_title="RockyBot", page_icon="📈")

st.title("📈 RockyBot - News Research Tool")

st.sidebar.header("News URLs")

urls = []

for i in range(3):
    url = st.sidebar.text_input(f"URL {i+1}")
    if url.strip():
        urls.append(url.strip())

process = st.sidebar.button("Process URLs")

FAISS_PATH = os.path.join("vector_store", "faiss_index")
os.makedirs("vector_store", exist_ok=True)

# -------------------------------------------------------
# LLM & EMBEDDINGS
# -------------------------------------------------------

@st.cache_resource
def load_llm():
    return ChatGroq(
        model_name="llama-3.1-8b-instant",
        temperature=0.2,
        max_tokens=1024
    )

@st.cache_resource
def load_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

llm = load_llm()
embeddings = load_embeddings()


@st.cache_resource
def get_prompt():
    return ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
    You are a helpful AI assistant.

    Answer ONLY using the provided context.

    Never use outside knowledge.

    If the answer is not found in the context, reply exactly:

    I don't know.

    Context:
    {context}
    """
                ),
                ("human", "{input}")
            ]
        )

# -------------------------------------------------------
# PROCESS DOCUMENTS
# -------------------------------------------------------

if process:

    start = time.time()

    if len(urls) == 0:
        st.warning("Please enter at least one URL.")
        st.stop()

    with st.spinner("Processing..."):

        try:
            loader = UnstructuredURLLoader(urls=urls)
            documents = loader.load()

        except Exception as e:
            st.error(f"Error loading URLs:\n{e}")
            st.stop()

        if not documents:
            st.error("No content could be extracted from the provided URLs.")
            st.stop()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=700,
            chunk_overlap=150
        )

        docs = splitter.split_documents(documents)

        if len(docs) == 0:
            st.error("No text chunks could be created.")
            st.stop()

        vectorstore = FAISS.from_documents(
            docs,
            embeddings
        )
        if os.path.exists(FAISS_PATH):
            shutil.rmtree(FAISS_PATH)

        vectorstore.save_local(FAISS_PATH)

        st.session_state.vectorstore = vectorstore
        st.session_state.processed = True

        st.success(f"Loaded {len(documents)} documents")
        st.caption(f"Created {len(docs)} text chunks.")

    end = time.time()

    st.success("Knowledge Base Ready!")

    st.success(f"Knowledge base created in {end - start:.2f} seconds")

    st.sidebar.success("Indexed URLs")

for url in urls:
    st.sidebar.write(url)

# -------------------------------------------------------
# QUESTION
# -------------------------------------------------------


if "processed" not in st.session_state:
    st.session_state.processed = False

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

question = st.text_input(
    "Ask a question",
    disabled=not st.session_state.processed
)

if not st.session_state.processed:
    st.info("⬅️ Enter article URLs and click Process.")

# -------------------------------------------------------
# RETRIEVAL
# -------------------------------------------------------

if question:

    if not os.path.exists(FAISS_PATH):
        st.error("Please process the URLs first.")
        st.stop()

    if st.session_state.vectorstore is None:
        st.session_state.vectorstore = FAISS.load_local(
            FAISS_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )

    vectorstore = st.session_state.vectorstore

    retriever = vectorstore.as_retriever()

    retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 4, "fetch_k": 10}
)

prompt = get_prompt()

docs = retriever.invoke(question)

context = "\n\n".join(doc.page_content for doc in docs)

chain = (
    prompt
    | llm
    | StrOutputParser()
)

with st.spinner("Generating answer..."):
    try:
        answer = chain.invoke(
            {
                "context": context,
                "input": question
            }
        )
    except Exception as e:
        st.error(f"Error: {e}")
        st.stop()

st.header("Answer")
st.write(answer)

with st.expander("Sources"):
    seen = set()

    for doc in docs:
        source = doc.metadata.get("source", "Unknown")

        if source not in seen:
            seen.add(source)
            st.markdown(f"• {source}")