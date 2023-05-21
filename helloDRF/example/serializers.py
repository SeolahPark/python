from rest_framework import serializers
from .models import Book

#모델의 내용을 기반으로 동작하는 시리얼라이저
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['bid', 'title', 'author', 'category', 'pages', 'price', 'published_date', 'description',]