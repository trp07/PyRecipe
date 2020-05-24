"""Handles all authentication requirements."""

from passlib.handlers.sha2_crypt import sha512_crypt as crypto


def hash_password(password: str) -> str:
    """Hash the given password and return the hash."""
    return _hash_text(password)


def _hash_text(text: str) -> str:
    """Hash the given text."""
    hashed_text = crypto.encrypt(text, rounds=121547)
    return hashed_text


def verify_password(plain_text: str, hashed_text: str) -> bool:
    """Verify the password hash corresponds to the supplied
    plaintext password."""
    return crypto.verify(plain_text, hashed_text)
