# 📄 Document Intelligence RAG System

A Retrieval-Augmented Generation (RAG) application that enables users to upload documents and ask natural language questions about their content. The system performs semantic search using embeddings and generates context-aware responses using Google's Gemini model.

---

# 🚀 Features

- Upload PDF documents
- Upload Word documents (.docx)
- Upload Text files (.txt)
- Upload CSV files (.csv)
- Automatic text extraction
- Document chunking
- Embedding generation using Sentence Transformers
- Semantic search using vector embeddings
- MongoDB storage
- Context-aware answers using Gemini
- Streamlit web interface

---

# 🛠️ Tech Stack

- Python
- Streamlit
- MongoDB
- Sentence Transformers
- Google Gemini API
- PyPDF
- Python-Docx
- Pandas

---

# 📂 Project Structure

```text
rag-document-system/

│
├── app.py
│
├── loaders/
│   ├── pdf_loader.py
│   ├── docx_loader.py
│   ├── txt_loader.py
│   └── csv_loader.py
│
├── db/
│   └── mongodb.py
│
├── rag/
│   ├── embedder.py
│   ├── ingest.py
│   └── query.py
│
├── .env
│
├── requirements.txt
│
└── README.md
```

---

# ⚙️ Installation

## Step 1: Clone the Repository

```bash
git clone <repository-url>
cd rag-document-system
```

## Step 2: Create Virtual Environment

```bash
python -m venv venv
```

## Step 3: Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux/Mac

```bash
source venv/bin/activate
```

## Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 📦 Required Libraries

```bash
pip install streamlit
pip install pymongo
pip install sentence-transformers
pip install google-generativeai
pip install python-dotenv
pip install pypdf
pip install python-docx
pip install pandas
pip install numpy
pip install openpyxl
```

Or install everything together:

```bash
pip install streamlit pymongo sentence-transformers google-generativeai python-dotenv pypdf python-docx pandas numpy openpyxl
```

---

# 🔑 Environment Variables

Create a `.env` file in the root directory.

```env
MONGO_URI=your_mongodb_connection_string

GEMINI_API_KEY=your_gemini_api_key
```

---

# ▶️ Running the Application

```bash
streamlit run app.py
```

The application will start at:

```text
http://localhost:8501
```

---

# 🔄 RAG Pipeline

```text
User Uploads Document
            ↓
Document Loader
            ↓
Text Extraction
            ↓
Chunking
            ↓
Embedding Generation
            ↓
MongoDB Storage
            ↓

User Question
            ↓
Question Embedding
            ↓
Similarity Search
            ↓
Relevant Chunks Retrieved
            ↓
Gemini LLM
            ↓
Final Answer
```

---

# 🧠 Working

## 1. Document Upload

The user uploads a document such as:

- PDF
- DOCX
- TXT
- CSV

## 2. Text Extraction

Text is extracted from the uploaded document.

## 3. Chunking

Large documents are divided into smaller chunks for efficient retrieval.

## 4. Embedding Generation

Sentence Transformers converts text chunks into vector embeddings.

## 5. Storage

Embeddings and document chunks are stored in MongoDB.

## 6. Query Processing

When the user asks a question:

- Question is converted into an embedding.
- Similarity search finds the most relevant chunks.

## 7. Response Generation

Relevant chunks are provided as context to Gemini.

Gemini generates an answer based on the retrieved information.

---



---

# 📈 Future Enhancements

- MongoDB Atlas Vector Search
- Multiple document support
- Excel file support
- Website URL ingestion
- Source citations
- Chat history
- Re-ranking
- Knowledge Graph Retrieval
- LlamaIndex integration

---

# 💡 Key Concepts Used

- Retrieval-Augmented Generation (RAG)
- Embeddings
- Semantic Search
- Vector Similarity Search
- Large Language Models (LLMs)
- Document Intelligence
- Natural Language Processing (NLP)

---

# 👨‍💻 Author
# [Uday Gangal](https://www.linkedin.com/in/uday-gangal-085877347/)
