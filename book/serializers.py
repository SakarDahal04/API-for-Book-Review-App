from rest_framework import serializers
from book.models import Book, Review
from account.models import User


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'summary', 'published_date', 'genre')


class UserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class ReviewSerializer(serializers.ModelSerializer):
    user = UserBasicSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'user', 'rating', 'comment', 'created_at')

        
class BookDetailSerializer(serializers.ModelSerializer):
    reviews_book = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ('id', 'user', 'title', 'author', 'summary', 'published_date', 'genre', 'reviews_book')

# class ReviewAllSerializer(serializers.ModelSerializer):
#     user = UserBasicSerializer(read_only=True)
#     book = BookDetailSerializer(read_only=True)
    
#     class Meta:
#         model = Review
#         fields = ('book', 'user', 'rating', 'comment', 'created_at')