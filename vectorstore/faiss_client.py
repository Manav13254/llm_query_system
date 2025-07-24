import faiss
import numpy as np

class FaissClient:
    def __init__(self, embedding_dim: int = 384):
        # Using inner product for cosine similarity on normalized vectors
        self.index = faiss.IndexFlatIP(embedding_dim)
        self.embedding_dim = embedding_dim
        self.ids = []  # Keep track of vector IDs for traceability

    def add_vectors(self, vectors: np.ndarray, ids: list[str]):
        """
        Add vectors to the FAISS index with associated IDs.
        Note: FAISS IndexFlatIP does not support IDs natively,
        so you need to maintain an external mapping for IDs.
        """
        faiss.normalize_L2(vectors)  # Ensure vectors are normalized
        self.index.add(vectors)
        self.ids.extend(ids)

    def search(self, query_vector: np.ndarray, top_k: int = 5):
        """
        Search similar vectors for the query vector.
        Returns: distances and indexes
        """
        faiss.normalize_L2(query_vector)
        distances, indices = self.index.search(query_vector, top_k)
        return distances, indices


# if __name__ == "__main__":
#     import numpy as np
#     client = FaissClient()
#     # Random normalized embeddings
#     vectors = np.random.rand(3, 384).astype(np.float32)
#     vectors = vectors / np.linalg.norm(vectors, axis=1, keepdims=True)
#     ids = ["vec1", "vec2", "vec3"]
#     client.add_vectors(vectors, ids)

#     q = vectors[0].reshape(1, -1)
#     distances, indices = client.search(q, top_k=2)
#     print("Distances:", distances)
#     print("Indices:", indices)
