import pytest

from backend.utils import encrypt_password, decrypt_password

@pytest.mark.benchmark(group="cifrado")
def test_encrypt_password(benchmark):
    plain_password = "200211"
    benchmark(encrypt_password, plain_password)

@pytest.mark.benchmark(group="descifrado")
def test_decrypt_password_benchmark(benchmark):
    plain_password = "200211"
    encrypted_password = encrypt_password(plain_password)
    benchmark(decrypt_password, encrypted_password)
    