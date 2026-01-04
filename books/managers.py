from django.db import models
from django.shortcuts import get_object_or_404


class BookManager(models.Manager):
    def create_book(self, user, **kwargs):
        return self.create(user=user, **kwargs)

    def update_book(self, book_id, new_title=None, new_pages=None, new_publication_year=None):
        book = get_object_or_404(self.model, id=book_id)
        if new_title:
            book.title = new_title
        if new_pages is not None:
            book.pages = new_pages
        if new_publication_year is not None:
            book.publication_year = new_publication_year
        book.save()
        return book

    def delete_book(self, book_id):
        book = get_object_or_404(self.model, id=book_id)
        book.delete()

    def get_all_books_list(self) -> list:
        return self.all()

    def search_books(self, title=None, genre=None, publication_year=None, pages=None):
        queryset = self.all()
        if title:
            queryset = queryset.filter(title__icontains=title)
        if genre:
            queryset = queryset.filter(genre=genre)
        if publication_year:
            queryset = queryset.filter(publication_year=publication_year)
        if pages:
            queryset = queryset.filter(pages=pages)
        return queryset

    def take_book(self, book_id):
        book = get_object_or_404(self.model, id=book_id)
        book.is_taken = True
        book.save()
        return book

    def return_book(self, book_id):
        book = get_object_or_404(self.model, id=book_id)
        book.is_taken = False
        book.save()
        return book
