from huggingface_hub import snapshot_download
from sentence_transformers import SentenceTransformer
import os

# Download the model files to local cache folder
model_name = "sentence-transformers/all-MiniLM-L6-v2"
cache_dir = snapshot_download(model_name, revision="main")  # 'main' is branch name

# Load model from cached local directory
model = SentenceTransformer(cache_dir)
tokenizer = model.tokenizer

CHUNK_SIZE = 300
OVERLAP = int(CHUNK_SIZE * 0.20)  # 60 tokens overlap

def chunk_text_sliding_window(text: str, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    token_ids = tokenizer.encode(text, add_special_tokens=False)
    chunks = []
    for start in range(0, len(token_ids), chunk_size - overlap):
        end = min(start + chunk_size, len(token_ids))
        chunk_tokens = token_ids[start:end]
        chunk_text = tokenizer.decode(chunk_tokens, skip_special_tokens=True)
        chunks.append({
            "text": chunk_text,
            "token_start": start,
            "token_end": end
        })
        if end == len(token_ids):
            break
    return chunks

# if __name__ == "__main__":
#     sample = "This is a sample text to demonstrate the sliding window chunking technique. " * 50
#     chunks = chunk_text_sliding_window(sample)
#     print(f"Generated {len(chunks)} chunks.")
#     for i, c in enumerate(chunks):
#         print(f"Chunk {i+1}: tokens {c['token_start']} to {c['token_end']}")
#         print(c['text'][:100] + "...\n")
