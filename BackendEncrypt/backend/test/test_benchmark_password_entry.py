import pytest
from rest_framework.test import APIClient
from django.urls import reverse, NoReverseMatch
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def test_user(db):
    user = User.objects.create_user(
        username='testuser', 
        email='testCRUD@gmail.com', 
        password='testpassword123'
    )
    return user

@pytest.fixture
def api_client(test_user):
    client = APIClient()
    client.force_authenticate(user=test_user)
    return client

# @pytest.fixture
# def sample_password_entry(api_client, test_user):
#     """Fixture que crea una entrada de contraseña para usar en tests"""
#     try:
#         url = reverse('passwordentry-list')
#     except NoReverseMatch:
#         pytest.skip("URL 'passwordentry-list' no encontrada")
    
#     data = {
#         "user": test_user.id,
#         "title": "Sample Entry",
#         "raw_password": "sample_secret"
#     }
    
#     response = api_client.post(url, data, format='json')
#     if response.status_code != 201:
#         pytest.fail(f"No se pudo crear entrada de prueba: {response.status_code}")
    
#     return response.data

@pytest.fixture
def sample_password_entry(api_client):
    """Fixture que crea una entrada de contraseña para usar en tests"""
    try:
        url = reverse('passwordentry-list')
    except NoReverseMatch:
        pytest.skip("URL 'passwordentry-list' no encontrada")
    
    data = {
        "title": "Sample Entry",
        "raw_password": "sample_secret"
    }
    
    response = api_client.post(url, data, format='json')
    print("Fixture: Entrada creada:", response.data)  # depuración opcional
    if response.status_code != 201:
        pytest.fail(f"No se pudo crear entrada de prueba: {response.status_code}")
    
    return response.data


@pytest.mark.django_db
def test_create_password_entry(api_client, test_user, benchmark):
    try:
        url = reverse('passwordentry-list')
    except NoReverseMatch:
        pytest.skip("URL 'passwordentry-list' no encontrada")
        
    data = {
        "user": test_user.id,
        "title": "Example Entry",
        "raw_password": "supersecret123"  
    }

    def create():
        response = api_client.post(url, data, format='json')
        assert response.status_code == 201
        assert response.data['title'] == data['title']
        assert 'id' in response.data

    benchmark(create)

@pytest.mark.django_db
def test_read_password_entries(api_client, sample_password_entry, benchmark):
    try:
        url = reverse('passwordentry-list')
    except NoReverseMatch:
        pytest.skip("URL 'passwordentry-list' no encontrada")

    def read():
        response = api_client.get(url)
        assert response.status_code == 200
        assert len(response.data) > 0

    benchmark(read)

@pytest.mark.django_db
def test_update_password_entry(api_client, test_user, sample_password_entry, benchmark):
    try:
        url_detail = reverse('passwordentry-detail', args=[sample_password_entry['id']])
    except NoReverseMatch:
        pytest.skip("URL 'passwordentry-detail' no encontrada")
    
    # Verificar que el objeto existe antes de actualizar
    get_response = api_client.get(url_detail)
    if get_response.status_code != 200:
        pytest.fail(f"El objeto no existe antes de actualizar: {get_response.status_code}")
    
    updated_data = {
        "user": test_user.id,
        "title": "Updated Entry",
        "raw_password": "newsecret123"
    }

    def update():
        response = api_client.put(url_detail, updated_data, format='json')
        assert response.status_code == 200
        assert response.data['title'] == updated_data['title']

    benchmark(update)

@pytest.mark.django_db
def test_delete_password_entry_simple(api_client, sample_password_entry):
    """Test DELETE que ejecuta siempre y muestra errores detallados"""

    # url_detail = reverse('passwordentry-detail', args=[sample_password_entry['id']])
    # url_detail = reverse('passwordentry-detail', args=[sample_password_entry['id']])

    try:
        url_detail = reverse('passwordentry-detail', args=[sample_password_entry['id']])
    except NoReverseMatch:
        print("ID sample:", sample_password_entry)
        pytest.fail("URL 'passwordentry-detail' no encontrada")
    
    # Verificar que el objeto existe
    get_response = api_client.get(url_detail)
    assert get_response.status_code == 200
    
    print(f"Objeto existe: {get_response.status_code}")
    
    # Ejecutar DELETE sin importar el resultado esperado
    delete_response = api_client.delete(url_detail)
    print(f"DELETE response: {delete_response.status_code}")
    
    # Mostrar detalles del error si no es el esperado
    if delete_response.status_code != 204:
        print(f"DELETE falló. Status: {delete_response.status_code}")
        print(f"Response headers: {dict(delete_response.headers)}")
        
        # Mostrar el contenido de la respuesta si existe
        if hasattr(delete_response, 'data') and delete_response.data:
            print(f"Response data: {delete_response.data}")
        elif hasattr(delete_response, 'content') and delete_response.content:
            print(f"Response content: {delete_response.content.decode('utf-8')}")
        
        # Proporcionar información específica sobre diferentes códigos de error
        if delete_response.status_code == 405:
            print("ERROR: Método DELETE no permitido. El ViewSet no soporta eliminación.")
            print("Verifica que tu ViewSet incluya 'destroy' en los métodos permitidos.")
        elif delete_response.status_code == 404:
            print("ERROR: Objeto no encontrado para DELETE.")
            print("Verifica la configuración del ViewSet y las URLs.")
        elif delete_response.status_code == 403:
            print("ERROR: Permisos insuficientes para DELETE.")
            print("Verifica los permisos en el ViewSet.")
        elif delete_response.status_code == 500:
            print("ERROR: Error interno del servidor durante DELETE.")
            print("Revisa los logs del servidor para más detalles.")
        
        # Fallar la prueba con información detallada
        pytest.fail(f"DELETE falló con código {delete_response.status_code}. Ver detalles arriba.")
    
    # Si llegamos aquí, el DELETE fue exitoso
    print("DELETE exitoso!")
    
    # Verificar que se eliminó
    final_get = api_client.get(url_detail)
    if final_get.status_code != 404:
        print(f"ADVERTENCIA: El objeto aún existe después del DELETE. Status: {final_get.status_code}")
        pytest.fail(f"El objeto no se eliminó correctamente. Status después de DELETE: {final_get.status_code}")
    
    print("Verificación final: El objeto fue eliminado correctamente.")