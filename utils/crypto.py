import hashlib
import bcrypt
import base64
import urllib.parse
import html
import re
from typing import Optional
import argon2
import os


def hash_password(password: str, algorithm: str) -> str:
    """Hash a password using the specified algorithm"""
    password_bytes = password.encode("utf-8")

    if algorithm == "md5":
        return hashlib.md5(password_bytes).hexdigest()
    elif algorithm == "sha1":
        return hashlib.sha1(password_bytes).hexdigest()
    elif algorithm == "sha256":
        return hashlib.sha256(password_bytes).hexdigest()
    elif algorithm == "sha512":
        return hashlib.sha512(password_bytes).hexdigest()
    elif algorithm == "bcrypt":
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password_bytes, salt).decode("utf-8")
    elif algorithm == "scrypt":
        # Using hashlib's scrypt (available in Python 3.6+)
        salt = os.urandom(16)
        hashed_password = hashlib.scrypt(
            password_bytes,
            salt=salt,
            n=2**14,  # CPU/memory cost parameter
            r=8,  # Block size parameter
            p=1,  # Parallelization parameter
            dklen=64,
        )
        return salt.hex() + "$" + hashed_password.hex()
    elif algorithm == "argon2":
        ph = argon2.PasswordHasher()
        return ph.hash(password_bytes)
    else:
        raise ValueError(f"Unsupported algorithm: {algorithm}")


def verify_password(password: str, hash_value: str, algorithm: str) -> bool:
    """Verify a password against a hash"""
    try:
        if algorithm in ["md5", "sha1", "sha256", "sha512"]:
            return hash_password(password, algorithm) == hash_value
        elif algorithm == "bcrypt":
            return bcrypt.checkpw(password.encode("utf-8"), hash_value.encode("utf-8"))
        elif algorithm == "scrypt":
            try:
                salt_hex, hashed_password_hex = hash_value.split("$")
                salt = bytes.fromhex(salt_hex)
                password_bytes = password.encode("utf-8")
                new_hash = hashlib.scrypt(
                    password_bytes,
                    salt=salt,
                    n=2**14,
                    r=8,
                    p=1,
                    dklen=64,
                )
                return new_hash.hex() == hashed_password_hex
            except:
                return False
        elif algorithm == "argon2":
            ph = argon2.PasswordHasher()
            return ph.verify(hash_value, password.encode("utf-8"))
        else:
            return False
    except:
        return False


def identify_hash_type(hash_string: str) -> Optional[str]:
    """Attempt to identify the hash type"""
    hash_string = hash_string.strip()

    # Length-based identification
    if len(hash_string) == 32 and re.match(r"^[a-f0-9]{32}$", hash_string):
        return "md5"
    elif len(hash_string) == 40 and re.match(r"^[a-f0-9]{40}$", hash_string):
        return "sha1"
    elif len(hash_string) == 64 and re.match(r"^[a-f0-9]{64}$", hash_string):
        return "sha256"
    elif len(hash_string) == 128 and re.match(r"^[a-f0-9]{128}$", hash_string):
        return "sha512"
    elif (
        hash_string.startswith("$2a$")
        or hash_string.startswith("$2b$")
        or hash_string.startswith("$2y$")
    ):
        return "bcrypt"
    elif hash_string.startswith("$argon2"):
        return "argon2"
    elif re.match(r"^[a-f0-9]{32}\$[a-f0-9]{128}$", hash_string):
        return "scrypt"

    return None


def base64_encode(data: str) -> str:
    """Base64 encode data"""
    return base64.b64encode(data.encode("utf-8")).decode("utf-8")


def base64_decode(data: str) -> str:
    """Base64 decode data"""
    try:
        return base64.b64decode(data.encode("utf-8")).decode("utf-8")
    except:
        return "Invalid Base64 data"


def url_encode(data: str) -> str:
    """URL encode data"""
    return urllib.parse.quote(data)


def url_decode(data: str) -> str:
    """URL decode data"""
    return urllib.parse.unquote(data)


def html_encode(data: str) -> str:
    """HTML encode data"""
    return html.escape(data)


def html_decode(data: str) -> str:
    """HTML decode data"""
    return html.unescape(data)


def hex_encode(data: str) -> str:
    """Hex encode data"""
    return data.encode("utf-8").hex()


def hex_decode(data: str) -> str:
    """Hex decode data"""
    try:
        return bytes.fromhex(data).decode("utf-8")
    except:
        return "Invalid hex data"
