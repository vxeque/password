from django.test import TestCase
from memory_profiler import memory_usage
from myapp.models import Usuario

class MemoryUsageCRUDTests(TestCase):

    def test_crear_usuario_memory(self):
        def crear():
            Usuario.objects.create(nombre="Juan", email="juan@example.com")

        mem = memory_usage(crear, interval=0.1)
        print(f"[CREATE] Uso de memoria: {max(mem) - min(mem):.4f} MiB")

    def test_leer_usuario_memory(self):
        Usuario.objects.create(nombre="Ana", email="ana@example.com")
        
        def leer():
            list(Usuario.objects.filter(nombre="Ana"))

        mem = memory_usage(leer, interval=0.1)
        print(f"[READ] Uso de memoria: {max(mem) - min(mem):.4f} MiB")

    def test_actualizar_usuario_memory(self):
        user = Usuario.objects.create(nombre="Luis", email="luis@example.com")
        
        def actualizar():
            user.nombre = "Luis Actualizado"
            user.save()

        mem = memory_usage(actualizar, interval=0.1)
        print(f"[UPDATE] Uso de memoria: {max(mem) - min(mem):.4f} MiB")

    def test_eliminar_usuario_memory(self):
        user = Usuario.objects.create(nombre="Mario", email="mario@example.com")

        def eliminar():
            user.delete()

        mem = memory_usage(eliminar, interval=0.1)
        print(f"[DELETE] Uso de memoria: {max(mem) - min(mem):.4f} MiB")
