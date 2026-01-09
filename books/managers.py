from django.db import models



class BookManager(models.Manager):
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
