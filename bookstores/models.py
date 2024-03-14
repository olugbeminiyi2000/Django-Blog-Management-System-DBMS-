from django.db import models

# Create your models here.

class Author(models.Model):
    author = models.CharField(max_length=150, null=False, unique=True)


class Language(models.Model):
    LANGUAGE_CHOICES = [
        ("en", "English"),
        ("fr", "French"),
        ("rw", "Kinyarwanda"),
    ]
    language = models.CharField(max_length=2, null=False, choices=LANGUAGE_CHOICES)


class Status(models.Model):
    STATUS_CHOICES = [
        ("AVL", "Available"),
        ("ONL", "On Loan"),
        ("RES", "Reserved"),
    ]
    status = models.CharField(max_length=3, null=False, choices=STATUS_CHOICES)


class Book(models.Model):
    book = models.CharField(max_length=150, null=False, unique=True)
    author_name = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        null=False,
        related_name="books",
    )
    language_name = models.ForeignKey(
        Language,
        models.SET_NULL,
        null=True,
        related_name="books_written",
    )

    
class Instance(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    book_name = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        null=False,
        related_name="copies",
    )
    status_name = models.ForeignKey(
        Status,
        on_delete=models.SET_NULL,
        null=True,
        related_name="books_status",
    )
