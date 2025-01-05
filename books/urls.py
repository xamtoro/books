from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import BookViewSet
from .auth_views import register
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')

urlpatterns = [
    # Endpoint para registro
    path('auth/register/', register, name='register'),
    # Endpoint para obtener tokens (inicio de sesión)
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Endpoint para refrescar el token
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# Añade las rutas del router
urlpatterns += router.urls