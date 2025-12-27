from django.db import models
from django.shortcuts import get_object_or_404

from books.models import Book


class BookManager(models.Model):
    def create_book(self, user, title, genre, pages, publication_year):
        return self.create(
            user=user,
            title=title,
            genre=genre,
            pages=pages,
            publication_year=publication_year
        )

    def update_book(self, book_id, new_title=None, new_pages=None, new_publication_year=None):
        book = get_object_or_404(Book, id=book_id)
        if new_title:
            book.title = new_title
        if new_pages is not None:
            book.pages = new_pages
        if new_publication_year is not None:
            book.publication_year = new_publication_year
        book.save()

    def delete_book(self, book_id):
        book = get_object_or_404(Book, id=book_id)
        book.delete()
