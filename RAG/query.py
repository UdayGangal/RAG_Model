import numpy as np

from db.mongodb import collection

from rag.embedder import create_embedding

def cosine_similarity(a, b):

    a = np.array(a)

    b = np.array(b)

    return np.dot(a, b) / (
        np.linalg.norm(a)
        * np.linalg.norm(b)
    )


def retrieve(query):

    query_embedding = create_embedding(query)

    docs = list(collection.find())

    scored = []

    for doc in docs:

        score = cosine_similarity(
            query_embedding,
            doc["embedding"]
        )

        scored.append(
            (score, doc)
        )

    scored.sort(
        reverse=True,
        key=lambda x: x[0]
    )

    return scored[:3]