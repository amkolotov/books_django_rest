from django.db import models
from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend

from .models import Book, Author
from .serializers import BookListSerializer, BookDetailSerializer, ReviewCreateSerializer, RatingCreateSerializer, \
    AuthorListSerializer, AuthorDetailSerializer
from .service import get_ip, BookFilter, PaginationBook


class BookListView(generics.ListAPIView):
    """Вывод списка книг"""

    serializer_class = BookListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BookFilter
    pagination_class = PaginationBook

    def get_queryset(self):
        # books = Book.objects.filter(draft=False).annotate(
        #     rating_user=models.Case(
        #         models.When(ratings__ip=get_ip(self.request), then=True),
        #         default=False,
        #         output_field=models.BooleanField()
        #     )
        # )
        books = Book.objects.filter(draft=False).annotate(
            rating_user=models.Count('ratings', filter=models.Q(ratings__ip=get_ip(self.request)))
        ).annotate(
            middle_rating=models.Sum(models.F('ratings__rating')) / models.Count(models.F('ratings'))
        )

        return books


class BookDetailView(generics.RetrieveAPIView):
    """Вывод информации о книге"""

    serializer_class = BookDetailSerializer

    def get_queryset(self):
        books = Book.objects.filter(draft=False).annotate(
            rating_user=models.Count('ratings', filter=models.Q(ratings__ip=get_ip(self.request)))
        ).annotate(
            middle_rating=models.Sum(models.F('ratings__rating')) / models.Count(models.F('ratings'))
        )

        return books


class ReviewCreateView(generics.CreateAPIView):
    """Добавление отзыва к книге"""
    serializer_class = ReviewCreateSerializer


class AddRatingView(generics.CreateAPIView):
    """Добавление рейтинга к книге"""
    serializer_class = RatingCreateSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_ip(self.request))


class AuthorListView(generics.ListAPIView):
    """Вывод списка авторов"""
    queryset = Author.objects.all()
    serializer_class = AuthorListSerializer
    # permission_classes = [permissions.IsAuthenticated]


class AuthorDetailView(generics.RetrieveAPIView):
    """Вывод информации об авторе"""
    queryset = Author.objects.all()
    serializer_class = AuthorDetailSerializer

