from sentence_transformers import SentenceTransformer
import numpy as np

class LocalEmbedder:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2", device: str = "cpu"):
        self.model = SentenceTransformer(model_name, device=device)

    def embed_batch(self, texts: list[str]) -> np.ndarray:
        """
        Given a list of text chunks, generate normalized embeddings.
        """
        embeddings = self.model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
        return embeddings

if __name__ == "__main__":
    embedder = LocalEmbedder()
    sample_texts = [
        "This is the first test chunk.",
        "Here is another chunk of text to embed."
    ]
    embeddings = embedder.embed_batch(sample_texts)
    print("Embeddings shape:", embeddings.shape)  # Should be (2, 384)
