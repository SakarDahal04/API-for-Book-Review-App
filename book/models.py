from django.db import models
from account.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Book(models.Model):
    """To store the detail about the book"""
    title = models.CharField(max_length=256)
    author = models.CharField(max_length=256)
    summary = models.TextField()
    published_date = models.DateField()
    genre = models.CharField(max_length=20)
    user = models.ForeignKey(User, related_name="book_user", on_delete=models.CASCADE, null=True, blank=True)
    isbn = models.CharField(max_length=13, null=True, blank=True)

    def __str__(self):
        return f"Instance of {self.title} book"
    
class Review(models.Model):
    """Review for the book provided by the user."""
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews_book")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews_user")
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Instance of comment {self.comment}"