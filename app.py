import streamlit as st

from loaders.pdf_loader import load_pdf
from loaders.docx_loader import load_docx
from loaders.txt_loader import load_txt
from loaders.csv_loader import load_csv

from rag.ingest import ingest_document
from rag.query import retrieve

import google.generativeai as genai
from dotenv import load_dotenv

import os

load_dotenv()

genai.configure(
    api_key=os.getenv(
        "GEMINI_API_KEY"
    )
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

st.title(
    "Document Intelligence RAG"
)

uploaded_file = st.file_uploader(
    "Upload Document",
    type=["pdf","docx","txt","csv"]
)

if uploaded_file:

    path = uploaded_file.name

    with open(path, "wb") as f:

        f.write(
            uploaded_file.getbuffer()
        )

    if path.endswith(".pdf"):

        text = load_pdf(path)

    elif path.endswith(".docx"):

        text = load_docx(path)

    elif path.endswith(".txt"):

        text = load_txt(path)

    else:

        text = load_csv(path)

    ingest_document(
        text,
        uploaded_file.name
    )

    st.success(
        "Document Indexed"
    )

question = st.text_input(
    "Ask Question"
)

if st.button("Ask"):

    results = retrieve(question)

    context = "\n".join(
        [
            r[1]["text"]
            for r in results
        ]
    )

    prompt = f"""
    Context:
    {context}

    Question:
    {question}

    Answer only from context.
    """

    response = model.generate_content(
        prompt
    )

    st.subheader("Answer")

    st.write(response.text)

    st.subheader("Sources")

    for _, doc in results:

        st.write(doc["source"])