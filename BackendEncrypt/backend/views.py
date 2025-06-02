from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import PasswordEntry, User
from .serializer import PasswordEntrySerializer, UserSerializer, CustomTokenObtainPairSerializer

from .serializer import *

# Vista para gestionar usuarios
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Vista para gestionar entradas de contraseñas
class PasswordEntryViewSet(viewsets.ModelViewSet):
    serializer_class = PasswordEntrySerializer
    permission_classes = [IsAuthenticated]
    queryset = PasswordEntry.objects.none()  

    def get_queryset(self):
        return PasswordEntry.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

from rest_framework_simplejwt.views import TokenObtainPairView

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

