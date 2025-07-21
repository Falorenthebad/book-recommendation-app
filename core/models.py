# core/models.py

import ast
from django.db import models

class Book(models.Model):
    book_id          = models.IntegerField(primary_key=True)
    title            = models.CharField(max_length=255)
    author_names     = models.CharField(max_length=255)
    average_rating   = models.FloatField()
    ratings_count    = models.IntegerField()
    num_pages        = models.IntegerField(null=True, blank=True)
    publication_year = models.IntegerField(null=True, blank=True)
    genre_1          = models.CharField(max_length=100, null=True, blank=True)
    genre_2          = models.CharField(max_length=100, null=True, blank=True)
    genre_3          = models.CharField(max_length=100, null=True, blank=True)
    genre_4          = models.CharField(max_length=100, null=True, blank=True)
    genre_5          = models.CharField(max_length=100, null=True, blank=True)
    image_url        = models.URLField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"{self.title} — {self.first_author}"

    @property
    def authors_list(self):
        """
        author_names içinde eğer list of dict varsa dict['author']'ı,
        eğer list of string ise direkt string'i al, değilse raw string.
        """
        try:
            parsed = ast.literal_eval(self.author_names)
            if isinstance(parsed, list):
                out = []
                for e in parsed:
                    if isinstance(e, dict):
                        out.append(e.get('author', '') or '')
                    else:
                        out.append(str(e))
                return out
        except (ValueError, SyntaxError):
            pass
        return [self.author_names]

    @property
    def first_author(self):
        lst = self.authors_list
        return lst[0] if lst else ""
