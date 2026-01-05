from django.db import models
from django.shortcuts import get_object_or_404
from .constants import MAX_NUMBER_ISBN


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

    def change_is_taken(self, book_id):
        book = self.model.objects.filter(id=book_id).first()
        if book is None:
            raise ValueError("Книга не существует.")
        if book.is_taken:
            books_updated = self.model.objects.filter(id=book_id, is_taken=True).update(is_taken=False)
            if books_updated == 0:
                raise ValueError("Ошибка при обновлении статуса книги.")
        else:
            books_updated = self.model.objects.filter(id=book_id, is_taken=False).update(is_taken=True)
            if books_updated == 0:
                raise ValueError("Книга уже взята или не существует.")
        return self.model.objects.get(id=book_id)

    def clean_isbn(self):
        if not self.isbn:
            return ""
        isbn = self.replace(" ", "").replace("-", "").removeprefix("ISBN")
        if len(isbn) != MAX_NUMBER_ISBN:
            raise ValueError("Количество цифр в номере ISBN некорректное.")
        return isbn
