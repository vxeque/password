from rest_framework.routers import DefaultRouter
from .views import PasswordEntryViewSet, UserViewSet, CustomTokenObtainPairView

from django.urls import path, include
from .views import UserViewSet, PasswordEntryViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'passwords', PasswordEntryViewSet, basename='passwordentry')
# router.register(r'passwords', PasswordEntryViewSet)

# urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
     path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
]
