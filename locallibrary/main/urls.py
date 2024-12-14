from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthorViewSet, GenreViewSet, BookViewSet

# Создаем маршрутизатор
router = DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'books', BookViewSet)

# Добавляем маршруты в urlpatterns
urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
]