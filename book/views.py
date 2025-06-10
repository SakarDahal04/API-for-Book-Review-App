from django.shortcuts import get_object_or_404
from django.db.models import Prefetch

from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from book.serializers import BookSerializer, BookDetailSerializer, ReviewSerializer
from book.models import Book, Review

from drf_spectacular.utils import extend_schema


class BookListAPIView(APIView):
    """APIView to get all the books for the main page of the website"""
    
    @extend_schema(
        request=BookSerializer,  # Define expected request data
        responses={200: BookSerializer},  # Define response schema
        description="This API retrieves or processes data based on BookSerializer."
    )


    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookCreateAPIView(APIView):
    """
    Creates a book which will be related to the specific user
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = BookSerializer()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetailAPIView(APIView):
    """Returns all of the information about the book and reviews related to the book too"""
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            book = Book.objects.prefetch_related(
                Prefetch("reviews_book", queryset=Review.objects.select_related("user"))
            ).get(id=pk)

            serializer = BookDetailSerializer(book)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Book.DoesNotExist:
            return Response(
                {"error": "Book Not Found"}, status=status.HTTP_404_NOT_FOUND
            )


# From the profile page
class UserBookAPIView(APIView):
    """To see all the books that the user created themselves"""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        books = Book.objects.select_related("user").filter(user__id=pk)

        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserBookDeleteAPIView(APIView):
    """To delete the book from the database. The book should belong to the user i.e created by the user"""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        book = get_object_or_404(Book, id=pk)

        return Response(
            {"message": f"Do you really want to delete book {book.title}?"},
            status=status.HTTP_200_OK,
        )

    def delete(self, request, pk):
        book = get_object_or_404(Book, pk=pk)

        if book.user != request.user:
            return Response(
                {"error": "You are not allowed to delete this book"},
                status=status.HTTP_403_FORBIDDEN,
            )

        book.delete()
        return Response(
            {"message": "Book deleted Successfully"}, status=status.HTTP_204_NO_CONTENT
        )


class ReviewCreateAPIView(APIView):
    """Add the review which will be related to one specific books by the user."""
    permission_classes = [IsAuthenticated]

    def get(self, request, book_id):
        serializer = ReviewSerializer()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, book_id):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            book = get_object_or_404(Book, id=book_id)
            serializer.save(user=request.user, book=book)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewDeleteAPIView(APIView):
    """To delete the review provided on the book. The review should be of the user who want to delete it."""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        return Response(
            {"message": "Do you really want to delete this review?"},
            status=status.HTTP_200_OK,
        )

    def delete(self, request, pk):
        try:
            review = get_object_or_404(Review, id=pk)

            if review.user != request.user:
                return Response(
                    {"error": "Your don't have the permission to delete this review"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            review.delete()
            return Response(
                {"message": "Review deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )

        except Review.DoesNotExist:
            return Response(
                {"error": "This review doesn't exists."},
                status=status.HTTP_404_NOT_FOUND,
            )
