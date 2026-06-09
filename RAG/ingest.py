from rag.embedder import create_embedding
from db.mongodb import collection

def chunk_text(
    text,
    chunk_size=500
):

    chunks = []

    for i in range(
        0,
        len(text),
        chunk_size
    ):

        chunks.append(
            text[i:i+chunk_size]
        )

    return chunks


def ingest_document(
    text,
    source_name
):

    chunks = chunk_text(text)

    docs = []

    for chunk in chunks:

        docs.append({

            "source": source_name,

            "text": chunk,

            "embedding":
            create_embedding(chunk)

        })

    if docs:

        collection.insert_many(docs)