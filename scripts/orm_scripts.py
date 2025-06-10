from django.utils import timezone
from django.db import connection
from pprint import pprint

from book.models import Book,Review
from django.contrib.auth.models import User
from book.serializers import BookSerializer

def run():
    book = Book.objects.last()
    reviews = Review.objects.select_related('book', 'user').filter(book=book, user__username="Sakar")
    print(reviews)

    book.pop()
    
    pprint(connection.queries)