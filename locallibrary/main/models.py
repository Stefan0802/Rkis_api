from django.db import models

class Author(models.Model):
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    birthday = models.DateField(blank=True, null=False)
    death_day = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Genre(models.Model):
    name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100, blank=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    release_date = models.PositiveIntegerField(blank=True, null=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    category = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    file = models.FileField(upload_to='files/', blank=True, null=True)

    def __str__(self):
        return self.title