from typing import Dict
from db.session import SessionLocal
from db.models import DocumentChunk
from ingestion.chunker import chunk_text_sliding_window
from vectorstore.embedder import LocalEmbedder
from vectorstore.faiss_client import FaissClient
import numpy as np

embedder = LocalEmbedder()
faiss_client = FaissClient()

def process_document(doc_id: int, raw_text: str, meta: Dict):
    chunks = list(chunk_text_sliding_window(raw_text))
    if not chunks:
        return

    chunk_metas = []
    chunk_texts = []
    for idx, chunk in enumerate(chunks):
        chunk_metas.append({
            "doc_id": doc_id,
            "chunk_index": idx,
            "token_start": chunk["token_start"],
            "token_end": chunk["token_end"],
            "page": meta.get("page"),
            "clause_id": meta.get("clause_id"),
            "source_hash": meta.get("source_hash"),
            "text": chunk["text"],
            "embedded": False
        })
        chunk_texts.append(chunk["text"])

    session = SessionLocal()
    try:
        session.bulk_insert_mappings(DocumentChunk, chunk_metas)
        session.commit()
        db_chunks = session.query(DocumentChunk).filter(
            DocumentChunk.doc_id == doc_id
        ).order_by(DocumentChunk.chunk_index).all()

        batch_size = 100
        for i in range(0, len(chunk_texts), batch_size):
            batch_texts = chunk_texts[i:i+batch_size]
            batch_ids = [str(c.id) for c in db_chunks[i:i+batch_size]]
            embeddings = embedder.embed_batch(batch_texts)
            faiss_client.add_vectors(np.array(embeddings).astype('float32'), batch_ids)
            session.query(DocumentChunk).filter(DocumentChunk.id.in_(batch_ids)).update(
                {"embedded": True}, synchronize_session=False)
            session.commit()
    finally:
        session.close()

