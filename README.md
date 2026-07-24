# 📈 RockyBot – AI News Research Assistant

RockyBot is a Retrieval-Augmented Generation (RAG) application that allows users to analyze multiple news articles and ask natural language questions about their content.

The application extracts text from news URLs, generates semantic embeddings, stores them in a FAISS vector database, retrieves the most relevant document chunks, and uses a Groq-hosted Llama model to generate context-aware answers.

---

# 🚀 Live Demo

🔗 **Application:** https://article-chatbot-f5sszw23cfzxtru5xgk7yz.streamlit.app

Try the application live to:
- 🌐 Process news article URLs
- 🤖 Ask questions about the articles
- 📚 Retrieve context-aware answers using RAG
- 🔍 View the article sources used for generating responses

--

## 🚀 Features

- 🌐 Load and analyze up to 3 news article URLs
- 📄 Automatic webpage text extraction
- ✂️ Intelligent text chunking
- 🔍 Semantic search using FAISS Vector Database
- 🤖 LLM-powered question answering using Groq Llama 3.1
- 📚 Displays article sources used to generate answers
- ⚡ Fast retrieval using Maximum Marginal Relevance (MMR)
- 🎯 Streamlit-based interactive UI

---

## 🏗️ Architecture

```
                 User URLs
                      │
                      ▼
        UnstructuredURLLoader
                      │
                      ▼
     RecursiveCharacterTextSplitter
                      │
                      ▼
      HuggingFace Embeddings
 (all-MiniLM-L6-v2 Sentence Transformer)
                      │
                      ▼
             FAISS Vector Store
                      │
                      ▼
          Semantic Retriever (MMR)
                      │
                      ▼
              Prompt Template
                      │
                      ▼
         Groq Llama-3.1-8B-Instant
                      │
                      ▼
              Final Answer
```

---

# 🛠️ Tech Stack

### Frontend

- Streamlit

### LLM

- Groq API
- Llama-3.1-8B-Instant

### Embeddings

- Sentence Transformers
- all-MiniLM-L6-v2

### Vector Database

- FAISS

### Framework

- LangChain

### Web Parsing

- Unstructured
- BeautifulSoup
- lxml

---

# 📂 Project Structure

```
RockyBot/
│
├── main.py
├── requirements.txt
├── .streamlit/
│      └── secrets.toml
│
├── vector_store/
│      └── faiss_index/
│
└── README.md
```

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/yourusername/RockyBot.git

cd RockyBot
```

Create a virtual environment

```bash
python -m venv venv
```

Activate

### Windows

```bash
venv\Scripts\activate
```

### Mac/Linux

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Configure API Key

Create

```
.streamlit/secrets.toml
```

Add your Groq API key

```toml
GROQ_API_KEY="your_groq_api_key"
```

---

# ▶️ Run the App

```bash
streamlit run main.py
```

---

# 💡 How It Works

### Step 1

Enter one or more news article URLs.

---

### Step 2

Click **Process URLs**.

The application:

- Downloads webpages
- Extracts article text
- Splits text into chunks
- Creates embeddings
- Stores embeddings inside FAISS

---

### Step 3

Ask any question.

Example:

```
What happened in the latest Nvidia earnings report?
```

---

### Step 4

The pipeline performs:

- Similarity Search
- Retrieves relevant chunks
- Builds prompt with context
- Sends prompt to Groq Llama
- Generates final answer

---

# 🧠 RAG Pipeline

```
News URLs
      │
      ▼
Document Loader
      │
      ▼
Chunking
      │
      ▼
Embeddings
      │
      ▼
FAISS
      │
      ▼
Retriever
      │
      ▼
Prompt
      │
      ▼
Groq LLM
      │
      ▼
Answer
```

---

# 📚 Libraries Used

- Streamlit
- LangChain
- LangChain Community
- LangChain Groq
- LangChain HuggingFace
- FAISS
- Sentence Transformers
- Transformers
- Torch
- BeautifulSoup4
- Unstructured
- Requests

---

# 📈 Future Improvements

- Conversation Memory
- PDF Upload Support
- Website Upload Support
- Hybrid Search (BM25 + Vector Search)
- Citation Highlighting
- Multi-turn Conversations
- Chat History
- Streaming Responses
- Docker Deployment
- Authentication
- Pinecone / Chroma Support

---

# 📸 Demo

### Process Articles

- Enter article URLs
- Click **Process URLs**

### Ask Questions

```
Summarize the article.

```

```
What are the key takeaways?

```

```
Who is mentioned in the article?

```

```
What is the company's future outlook?

```

---

# 🔍 Retrieval Strategy

The application uses **Maximum Marginal Relevance (MMR)** retrieval.

Benefits:

- Reduces duplicate context
- Improves answer diversity
- Better context coverage
- More relevant responses

Configuration:

```python
k = 4
fetch_k = 10
```

---

# 📊 Embedding Model

```
sentence-transformers/all-MiniLM-L6-v2
```

- 384-dimensional embeddings
- Lightweight
- Fast inference
- Excellent semantic similarity performance

---

# 🤖 LLM

```
Groq
```

Model

```
llama-3.1-8b-instant
```

Configuration

- Temperature: 0.2
- Max Tokens: 1024

---

# 🎯 Skills Demonstrated

- Retrieval-Augmented Generation (RAG)
- Large Language Models
- Prompt Engineering
- Vector Databases
- Semantic Search
- FAISS
- HuggingFace Embeddings
- Streamlit Development
- LangChain Expression Language (LCEL)
- AI Application Development
- Document Processing
- Information Retrieval

---

# 👨‍💻 Author

**Akhilesh Pal**

M.Sc. Statistics | AI Engineer | Data Scientist

GitHub: https://github.com/yourusername

LinkedIn: https://linkedin.com/in/yourprofile

---

## ⭐ If you found this project useful, consider giving it a Star.
