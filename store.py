import chromadb
from sentence_transformers import SentenceTransformer

EMBED_MODEL = "all-MiniLM-L6-v2"

# The embedding model is downloaded once on first run (about 90 MB)
model = SentenceTransformer(EMBED_MODEL)
client = chromadb.PersistentClient(path="chroma_db")


def get_collection(name="docmind"):
    return client.get_or_create_collection(
        name=name, metadata={"hnsw:space": "cosine"}
    )


def add_chunks(chunks, source):
    """Embed chunks and store them with their page number and source name."""
    collection = get_collection()
    texts = [c["text"] for c in chunks]
    embeddings = model.encode(texts).tolist()
    ids = [f"{source}-{i}" for i in range(len(chunks))]
    metadatas = [{"source": source, "page": c["page"]} for c in chunks]
    collection.upsert(
        ids=ids, documents=texts, embeddings=embeddings, metadatas=metadatas
    )
    return len(chunks)


def search(query, k=4):
    """Return the k chunks most similar in meaning to the query."""
    collection = get_collection()
    query_embedding = model.encode([query]).tolist()
    results = collection.query(query_embeddings=query_embedding, n_results=k)

    hits = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        hits.append(
            {
                "text": doc,
                "page": meta["page"],
                "source": meta["source"],
                "distance": dist,
            }
        )
    return hits

def reset_collection(name="docmind"):
    """Delete all stored chunks so a new document starts clean."""
    try:
        client.delete_collection(name)
    except Exception:
        pass
    return get_collection(name)

if __name__ == "__main__":
    from ingest import load_pdf, chunk_pages

    pages = load_pdf("sample.pdf")
    chunks = chunk_pages(pages)
    count = add_chunks(chunks, source="sample.pdf")
    print(f"Stored {count} chunks.")

    question = input("Ask something about your PDF: ")
    for hit in search(question):
        print(f"\n[Page {hit['page']}] (distance: {hit['distance']:.3f})")
        print(hit["text"][:300])