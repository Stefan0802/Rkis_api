from rest_framework import serializers, viewsets
from .models import Author, Genre, Book
from rest_framework import status
from rest_framework.response import Response
from .permissions import IsAdminUserOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

# Сериализатор  для жанров
class GenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

# Сериализатор для отображения в книгах только имени, фамилии, юрл автора
class AuthorUrlSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name = 'author-detail')

    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'url']

# Сериализатор для отоборажения книг
class BookSerializer(serializers.HyperlinkedModelSerializer):
    authors = AuthorUrlSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'release_date', 'genre', 'category', 'image', 'file', 'authors' ]  # Возвращаем поля книги

# Сериализатор для отображения в авторах только название и юрл книг(и)
class BookTitleUrlSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='book-detail')  # Убедитесь, что у вас есть соответствующий URL

    class Meta:
        model = Book
        fields = ['title', 'url']  # Возвращаем только название и URL

# Сериализатор  для отображения данных автора
class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    books = BookTitleUrlSerializer(many=True, read_only=True)  # Используем новый сериализатор

    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name', 'birthday', 'death_day', 'books']  # Добавляем поле books

# класс для авторов, который наследуется от 'viewsets.ModelViewSet' в REST он нужен для обработки запросов к модели Author представляя стандартные операции CRUD (создание, чтение, обновление и удаление)
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ['first_name', 'last_name']

    def create(self, request, *args, **kwargs):
        first_name_author = request.data.get('first_name')
        last_name_author = request.data.get('last_name')

        if Author.objects.filter(first_name=first_name_author, last_name=last_name_author).exists():
            return Response({"error": "Данный автор уже существует!"}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

# класс для жанров, который наследуется от 'viewsets.ModelViewSet' в REST он нужен для обработки запросов к модели Genre представляя стандартные операции CRUD (создание, чтение, обновление и удаление)
class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ['name']

    def create(self, request, *args, **kwargs):
        name_genre = request.data.get('name')

        if Genre.objects.filter(name=name_genre).exists():
            return Response({"error": "Жанр с таким названием уже существует!"}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

# класс для книг, который наследуется от 'viewsets.ModelViewSet' в REST он нужен для обработки запросов к модели Book представляя стандартные операции CRUD (создание, чтение, обновление и удаление)
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ['title', 'author__first_name']

    def create(self, request, *args, **kwargs):
        title_book = request.data.get('title')

        if Book.objects.filter(title=title_book).exists():
            return Response({"error": "Книга с таким названием и автором уже существует!"}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

