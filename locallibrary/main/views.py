from rest_framework import serializers, viewsets
from .models import Author, Genre, Book
from rest_framework import status
from rest_framework.response import Response
from .permissions import IsAdminUserOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter


class GenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class BookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class AuthorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Author
        fields = '__all__'



class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def create(self, request, *args, **kwargs):
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')

        if Author.objects.filter(first_name=first_name, last_name=last_name):
            return Response({"error": "Данный автор уже существует!"}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ['name']

    def create(self, request, *args, **kwargs):
        name = request.data.get('name')

        if Genre.objects.filter(name=name):
            return Response({"error": "Жанр с таким названием уже существует!"}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminUserOrReadOnly]  # Используем класс разрешений

    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ['title', 'author__first_name']

    def create(self, request, *args, **kwargs):
        title = request.data.get('title')

        if Book.objects.filter(title=title).exists():
            return Response({"error": "Книга с таким названием и автором уже существует!"}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

