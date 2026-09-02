# 🗂️ DocIQ — RAG-Powered Document Assistant

DocIQ is a **Retrieval-Augmented Generation (RAG)** application that allows users to upload documents and ask questions about their content.

The system extracts text from the uploaded document, divides it into smaller chunks, creates vector embeddings, stores them in MongoDB, retrieves the most relevant information, and generates an answer grounded in the uploaded document.

---

## 🚀 Features

- Upload and process multiple document formats
- Supports **PDF, DOCX, TXT, and CSV**
- Automatically extracts and chunks document text
- Generates semantic embeddings locally
- Stores document chunks and embeddings in MongoDB
- Retrieves relevant content using cosine similarity
- Uses Groq for fast LLM-based answer generation
- Generates answers only from the retrieved document context
- Displays the source document used for the answer
- Clean and responsive Streamlit interface
- Supports local and Docker-based deployment

---

## 🧠 What is RAG?

**Retrieval-Augmented Generation**, or RAG, improves an AI model by providing it with relevant information before it generates an answer.

Instead of asking the language model to answer using only its existing knowledge, DocIQ first searches the uploaded document for relevant content. That content is then passed to the language model as context.

This helps produce answers that are:

- More relevant
- Based on the uploaded document
- Less likely to contain hallucinated information
- Easier to verify

---

## ⚙️ How It Works

```text
Upload Document
       ↓
Extract Text
       ↓
Split Text into Chunks
       ↓
Generate Embeddings
       ↓
Store Chunks in MongoDB
       ↓
Convert User Question into an Embedding
       ↓
Calculate Cosine Similarity
       ↓
Retrieve Top 3 Relevant Chunks
       ↓
Send Context and Question to the LLM
       ↓
Generate a Grounded Answer
```

---

## 🏗️ System Architecture

```mermaid
flowchart TD
    A[Upload Document] --> B[Document Loader]
    B --> C[Text Chunking]
    C --> D[Sentence Transformer]
    D --> E[(MongoDB)]
    F[User Question] --> G[Question Embedding]
    G --> H[Cosine Similarity Search]
    E --> H
    H --> I[Top 3 Relevant Chunks]
    I --> J[Groq LLM]
    F --> J
    J --> K[Grounded Answer]
```

---

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| User Interface | Streamlit |
| Database | MongoDB |
| Embedding Model | Sentence Transformers |
| Embedding Model Name | `all-MiniLM-L6-v2` |
| Similarity Method | Cosine Similarity |
| Language Model API | Groq |
| LLM | `openai/gpt-oss-20b` |
| Containerization | Docker and Docker Compose |
| PDF Processing | PyPDF |
| Word Processing | python-docx |
| CSV Processing | Pandas |

---

## 📁 Project Structure

```text
RAG_Model/
│
├── app.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── test.py
├── .dockerignore
├── .env
│
├── db/
│   ├── __init__.py
│   └── mongodb.py
│
├── rag/
│   ├── __init__.py
│   ├── embedder.py
│   ├── ingest.py
│   └── query.py
│
└── loaders/
    ├── __init__.py
    ├── pdf_loader.py
    ├── docx_loader.py
    ├── txt_loader.py
    └── csv_loader.py
```

> Make sure the main Streamlit file is named `app.py`. If it is currently named `app(2).py`, rename it before running the application.

---

## 🔍 Main Components

### Document Loaders

The loader modules extract text from the uploaded files:

- `pdf_loader.py` extracts text from PDF files
- `docx_loader.py` extracts text from Word documents
- `txt_loader.py` reads plain-text files
- `csv_loader.py` converts CSV data into searchable text

### Text Chunking

The extracted text is divided into chunks of approximately **1,200 characters**.

Each chunk is processed separately so that the system can retrieve only the most relevant parts of a document.

### Embedding Generation

DocIQ uses the following Sentence Transformer model:

```text
sentence-transformers/all-MiniLM-L6-v2
```

The model converts every text chunk and user question into a numerical vector.

### MongoDB Storage

Every document chunk is stored in MongoDB with:

```json
{
  "source": "document-name.pdf",
  "text": "Extracted document content...",
  "embedding": [0.12, -0.08, 0.24]
}
```

### Semantic Retrieval

When a question is submitted:

1. The question is converted into an embedding.
2. Its cosine similarity is calculated against stored document embeddings.
3. The results are sorted by similarity score.
4. The top three chunks are returned as context.

### Answer Generation

The retrieved chunks and question are sent to the language model with instructions to answer only from the supplied context.

This reduces hallucinations and keeps the answer connected to the uploaded document.

---

## ✅ Prerequisites

Before running the project, install:

- Python 3.11 or later
- MongoDB
- Git
- Docker Desktop, if using Docker

You will also need a valid Groq API key.

---

## 💻 Local Installation

### 1. Clone the repository

```bash
git clone https://github.com/UdayGangal/RAG_Model.git
cd RAG_Model
```

### 2. Create a virtual environment

#### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### macOS or Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the root directory:

```env
MONGO_URI=mongodb://localhost:27017
GROQ_API_KEY=your_groq_api_key
```

> Never upload your real `.env` file or API keys to GitHub.

### 5. Start MongoDB

Make sure your MongoDB server is running locally on port `27017`.

### 6. Run the application

```bash
streamlit run app.py
```

Open the following address in your browser:

```text
http://localhost:8501
```

---

## 🐳 Running with Docker

Docker Compose starts both the Streamlit application and MongoDB.

### 1. Create the environment file

Create a `.env` file:

```env
MONGO_URI=mongodb://mongo:27017
GROQ_API_KEY=your_groq_api_key
```

### 2. Build and start the containers

```bash
docker compose up --build
```

To run the containers in the background:

```bash
docker compose up --build -d
```

### 3. Open the application

```text
http://localhost:8501
```

### 4. Stop the containers

```bash
docker compose down
```

To stop the containers and delete the MongoDB volume:

```bash
docker compose down -v
```

---

## 📖 How to Use

1. Open the DocIQ application.
2. Upload a PDF, DOCX, TXT, or CSV file.
3. Wait for the document to be indexed.
4. Enter a question related to the uploaded document.
5. Click the **Ask** button.
6. Review the generated answer and its source.

### Example Questions

```text
What is the main topic of this document?
```

```text
Summarize the key findings.
```

```text
What does the document say about machine learning?
```

```text
Explain the conclusion in simple language.
```

---

## 🗄️ MongoDB Configuration

DocIQ uses:

```text
Database: rag_db
Collection: documents
```

For local development:

```env
MONGO_URI=mongodb://localhost:27017
```

For Docker:

```env
MONGO_URI=mongodb://mongo:27017
```

A hosted MongoDB Atlas connection can also be used:

```env
MONGO_URI=mongodb+srv://username:password@cluster-url/rag_db
```

Do not commit a real MongoDB URI containing credentials.

---

## 📦 Main Dependencies

```text
streamlit
pymongo
python-dotenv
python-docx
pypdf
pandas
numpy
sentence-transformers
openai
```

Install all required packages using:

```bash
pip install -r requirements.txt
```

---

## 🧪 Testing the API Connection

The `test.py` file can be used to test an OpenAI API connection.

Run it using:

```bash
python test.py
```

> The current main application uses `GROQ_API_KEY`, while `test.py` uses `OPENAI_API_KEY`. Configure the appropriate variable depending on which file you are testing.

---

## 🔐 Security

Follow these security practices:

- Never commit the `.env` file
- Never expose API keys in source code
- Add `.env` to `.gitignore`
- Use environment variables for sensitive values
- Rotate an API key immediately if it is accidentally uploaded
- Avoid exposing MongoDB publicly without authentication

Recommended `.gitignore` content:

```gitignore
.env
.venv/
venv/
__pycache__/
*.pyc
.streamlit/
```

---

## ⚠️ Current Limitations

- Text is split using fixed character-based chunks
- All stored documents are searched during retrieval
- MongoDB vector search is not currently used
- Uploaded document records are not automatically removed
- Retrieval is performed in Python memory
- No user authentication is currently implemented
- No chat-history support is currently available
- Scanned PDFs require OCR, which is not currently included

---

## 🔮 Future Improvements

- Add paragraph-aware chunking with overlap
- Add MongoDB Atlas Vector Search
- Add a reranking stage
- Add retrieval-score thresholds
- Display similarity scores with sources
- Support multiple-document selection
- Add conversation history
- Add user authentication
- Add OCR support for scanned documents
- Add document deletion and collection management
- Add response streaming
- Add automated RAG evaluation
- Deploy the application to a cloud platform

---

## 🌟 Why This Project?

Large language models may generate incorrect information when they do not have access to the required data.

DocIQ addresses this problem using RAG. It retrieves relevant information from a user-provided document and supplies it to the language model before generating an answer.

This project demonstrates practical knowledge of:

- Retrieval-Augmented Generation
- Natural Language Processing
- Semantic search
- Embedding models
- MongoDB
- LLM API integration
- Streamlit application development
- Docker containerization

---

## 👨‍💻 Author

**Uday Gangal**

- GitHub: [UdayGangal](https://github.com/UdayGangal)
- Linkedin: [UdayGangal](www.linkedin.com/in/uday-gangal-085877347)

---

## 📄 License

This project is intended for educational and learning purposes.

You may add an open-source license, such as the MIT License, if you want others to reuse or modify the project.

---

## ⭐ Support

If you found this project useful, consider giving the repository a star.
