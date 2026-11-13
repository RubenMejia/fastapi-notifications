from app.core.security import hash_password, verify_password


def test_hash_is_not_the_password() -> None:
    hashed = hash_password("S3cret-pass")

    assert hashed != "S3cret-pass"
    assert hashed.startswith("$argon2id$")


def test_verify_accepts_the_right_password_only() -> None:
    hashed = hash_password("S3cret-pass")

    assert verify_password("S3cret-pass", hashed)
    assert not verify_password("wrong-pass", hashed)


def test_same_password_gives_different_hashes() -> None:
    assert hash_password("S3cret-pass") != hash_password("S3cret-pass")
