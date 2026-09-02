import streamlit as st

from loaders.pdf_loader import load_pdf
from loaders.docx_loader import load_docx
from loaders.txt_loader import load_txt
from loaders.csv_loader import load_csv

from rag.ingest import ingest_document
from rag.query import retrieve

from openai import OpenAI
from dotenv import load_dotenv
import os
import tempfile

load_dotenv()

# ── Page config ───────────────────────────────────────────────
st.set_page_config(
    page_title="DocIQ · RAG",
    page_icon="🗂",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global styles ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Hide default Streamlit header */
#MainMenu, footer, header { visibility: hidden; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0f1117;
    border-right: 1px solid #1e2130;
}
[data-testid="stSidebar"] * {
    color: #c9d1d9 !important;
}

/* Main area */
.main .block-container {
    padding: 2rem 2.5rem 3rem;
    max-width: 860px;
}

/* Page title */
.page-title {
    font-size: 1.6rem;
    font-weight: 600;
    color: #e6edf3;
    letter-spacing: -0.3px;
    margin-bottom: 0.2rem;
}
.page-subtitle {
    font-size: 0.85rem;
    color: #8b949e;
    margin-bottom: 2rem;
}

/* Divider */
.divider {
    border: none;
    border-top: 1px solid #21262d;
    margin: 1.5rem 0;
}

/* Answer card */
.answer-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-left: 3px solid #58a6ff;
    border-radius: 6px;
    padding: 1.1rem 1.4rem;
    font-size: 0.95rem;
    line-height: 1.7;
    color: #c9d1d9;
    margin-top: 0.8rem;
}

/* Source badge */
.source-badge {
    display: inline-block;
    background: #1c2128;
    border: 1px solid #30363d;
    border-radius: 4px;
    padding: 0.25rem 0.65rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: #8b949e;
    margin: 0.25rem 0.25rem 0.25rem 0;
}

/* Section labels */
.section-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #8b949e;
    margin-bottom: 0.5rem;
}

/* Upload area override */
[data-testid="stFileUploader"] {
    border: 1px dashed #30363d;
    border-radius: 6px;
    padding: 0.5rem;
    background: #0d1117;
}

/* Buttons */
.stButton > button {
    background: #238636;
    color: #fff;
    border: none;
    border-radius: 6px;
    padding: 0.45rem 1.2rem;
    font-size: 0.88rem;
    font-weight: 500;
    cursor: pointer;
    transition: background 0.15s;
}
.stButton > button:hover {
    background: #2ea043;
}

/* Text input */
.stTextInput > div > div > input {
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 6px;
    color: #c9d1d9;
    font-size: 0.92rem;
    padding: 0.5rem 0.75rem;
}
.stTextInput > div > div > input:focus {
    border-color: #58a6ff;
    box-shadow: 0 0 0 3px rgba(88,166,255,0.12);
}

/* Success / warning */
.stAlert {
    border-radius: 6px;
    font-size: 0.88rem;
}
</style>
""", unsafe_allow_html=True)

# ── Groq setup (via OpenAI-compatible endpoint) ─────────────────
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🗂 DocIQ")
    st.markdown("<div style='font-size:0.8rem;color:#8b949e;margin-bottom:1.5rem'>RAG-powered document assistant</div>", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("<div class='section-label'>Upload Document</div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        label="",
        type=["pdf", "docx", "txt", "csv"],
        label_visibility="collapsed"
    )

    if uploaded_file:
        st.markdown(f"""
        <div style='margin-top:0.8rem;padding:0.6rem 0.8rem;background:#1c2128;
             border:1px solid #30363d;border-radius:6px;font-size:0.82rem;color:#8b949e'>
            📄 <span style='color:#c9d1d9'>{uploaded_file.name}</span><br>
            <span style='font-size:0.75rem'>{round(uploaded_file.size/1024,1)} KB</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.75rem;color:#484f58;line-height:1.6'>
        Supported: PDF, DOCX, TXT, CSV<br>
        Answers are grounded in your document.
    </div>
    """, unsafe_allow_html=True)

# ── Main content ───────────────────────────────────────────────
st.markdown("<div class='page-title'>Document Intelligence</div>", unsafe_allow_html=True)
st.markdown("<div class='page-subtitle'>Ask questions about your uploaded document. Answers are generated from its content only.</div>", unsafe_allow_html=True)

# ── Ingest on upload ──────────────────────────────────────────
if uploaded_file:
    if "last_uploaded" not in st.session_state or st.session_state.last_uploaded != uploaded_file.name:
        with st.spinner("Indexing document…"):
            suffix = os.path.splitext(uploaded_file.name)[1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(uploaded_file.getbuffer())
                tmp_path = tmp.name

            if tmp_path.endswith(".pdf"):
                text = load_pdf(tmp_path)
            elif tmp_path.endswith(".docx"):
                text = load_docx(tmp_path)
            elif tmp_path.endswith(".txt"):
                text = load_txt(tmp_path)
            else:
                text = load_csv(tmp_path)

            os.unlink(tmp_path)
            ingest_document(text, uploaded_file.name)
            st.session_state.last_uploaded = uploaded_file.name

        st.success(f"**{uploaded_file.name}** indexed and ready.")

# ── Question area ─────────────────────────────────────────────
st.markdown("<hr class='divider'>", unsafe_allow_html=True)
st.markdown("<div class='section-label'>Ask a Question</div>", unsafe_allow_html=True)

col1, col2 = st.columns([5, 1])
with col1:
    question = st.text_input(
        label="",
        placeholder="e.g. What are the key findings in section 3?",
        label_visibility="collapsed"
    )
with col2:
    ask_clicked = st.button("Ask →", use_container_width=True)

# ── Answer ────────────────────────────────────────────────────
if ask_clicked:
    if not uploaded_file:
        st.warning("Upload a document first.")
    elif not question.strip():
        st.warning("Enter a question above.")
    else:
        with st.spinner("Retrieving context and generating answer…"):
            results = retrieve(question)

            if not results:
                st.info("No relevant content found in the document for that question.")
            else:
                context = "\n".join([r[1]["text"] for r in results])
                prompt = f"""Context:\n{context}\n\nQuestion:\n{question}\n\nAnswer only from the context provided. Be concise and precise."""

                try:
                    response = client.responses.create(
                        input=prompt,
                        model="openai/gpt-oss-20b",
                    )
                    answer_text = response.output_text
                except Exception as e:
                    st.error(f"Answer generation failed: {e}")
                    answer_text = None

                if answer_text:
                    st.markdown("<div class='section-label' style='margin-top:1.5rem'>Answer</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='answer-card'>{answer_text}</div>", unsafe_allow_html=True)

                    st.markdown("<div class='section-label' style='margin-top:1.5rem'>Sources</div>", unsafe_allow_html=True)
                    seen = set()
                    for _, doc in results:
                        src = doc["source"]
                        if src not in seen:
                            st.markdown(f"<span class='source-badge'>📄 {src}</span>", unsafe_allow_html=True)
                            seen.add(src)