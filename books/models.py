from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class BookStatus(models.TextChoices):
    OLD = "old"
    NEW = "new"
    DEFAULT = "not informed"


class Author(models.Model):
    name = models.CharField(max_length=255)

    # children tem que ser positivo entre 0 e 50
    # children = models.IntegerField(
    #     validators=[MinValueValidator(0), MaxValueValidator(50)]
    # )
    children = models.IntegerField()
    books = models.ManyToManyField("books.Book", related_name="authors")


# Create your models here.
class Book(models.Model):
    # Classe de configuração
    # class Meta:
    #     db_table = "novo_books"

    title = models.CharField(max_length=255)
    published_date = models.DateField()
    status = models.CharField(
        max_length=30, choices=BookStatus.choices, default=BookStatus.DEFAULT
    )
    isbn = models.CharField(max_length=13, unique=True)

    librarian = models.ForeignKey(
        "librarians.Librarian", on_delete=models.CASCADE, related_name="books"
    )
