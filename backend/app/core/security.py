from pwdlib import PasswordHash

# Argon2id with the library's recommended settings. The salt is random and stored inside the hash.
password_hash = PasswordHash.recommended()


def hash_password(raw: str) -> str:
    return password_hash.hash(raw)


def verify_password(raw: str, hashed: str) -> bool:
    return password_hash.verify(raw, hashed)
