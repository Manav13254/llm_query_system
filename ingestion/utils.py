import hashlib

def compute_sha256(filepath: str) -> str:
    """Compute the SHA-256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        # Read and update hash in chunks to avoid memory issues
        while True:
            data = f.read(65536)  # 64 KB chunks
            if not data:
                break
            sha256_hash.update(data)
    return sha256_hash.hexdigest()
