import pytest
from backend.models import User, PasswordEntry

@pytest.mark.django_db
def test_crear_password_entry_benchmark(benchmark):
    user = User.objects.create(email="test@example.com", username="testuser")
    raw_password="cave200211"

    def create_password_entry():
        create_entry = PasswordEntry(
            user=user, 
            title="Correo",
            username="usuario@mail.com",
            service_url="https://example.com",
            notes="Notas de ejemplo",
        )
        create_entry.set_password(raw_password)
        create_entry.save()

        benchmark(create_entry)

    