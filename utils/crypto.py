import hashlib


def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")

    sha256_hasher = hashlib.sha256()
    sha256_hasher.update(password_bytes)

    hashed_password = sha256_hasher.hexdigest()

    return hashed_password
