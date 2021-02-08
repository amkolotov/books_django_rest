from rest_framework import serializers

from .models import Book, Review, Rating, Author


class FilterReviewListSerializer(serializers.ListSerializer):
    """Фильтр комментариев,только родитель"""
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    """Рекурсивный вывод детей"""
    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(instance, context=self.context)
        return serializer.data


class AuthorListSerializer(serializers.ModelSerializer):
    """Вывод списка авторов"""
    class Meta:
        model = Author
        fields = ['id', 'name', 'image']


class AuthorDetailSerializer(serializers.ModelSerializer):
    """Вывод информации об авторе"""
    class Meta:
        model = Author
        fields = "__all__"


class BookListSerializer(serializers.ModelSerializer):
    """Список книг"""
    rating_user = serializers.BooleanField()
    middle_rating = serializers.IntegerField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'tagline', 'genres', 'rating_user', 'middle_rating', 'cover']


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Добавление отзыва к книге"""
    class Meta:
        model = Review
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    """Вывод отзывов"""
    children = RecursiveSerializer(many=True)

    class Meta:
        model = Review
        list_serializer_class = FilterReviewListSerializer
        fields = ['id', 'username', 'text', 'children']


class BookDetailSerializer(serializers.ModelSerializer):
    """Информация о книге"""
    genres = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    publisher = serializers.SlugRelatedField(slug_field='name', read_only=True)
    author = AuthorListSerializer(read_only=True)
    tag = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    reviews = ReviewSerializer(many=True)
    middle_rating = serializers.IntegerField()

    class Meta:
        model = Book
        fields = ['id', 'genres', 'publisher', 'author', 'tag', 'reviews', 'title', 'tagline', 'desc',
                  'num_of_pages', 'cover', 'year', 'slug', 'middle_rating']


class RatingCreateSerializer(serializers.ModelSerializer):
    """Добавление рейтинга к книге"""
    class Meta:
        model = Rating
        fields = ['rating', 'book']

    def create(self, validated_data):
        rating, _ = Rating.objects.update_or_create(
            ip=validated_data.get('ip', None),
            book=validated_data.get('book', None),
            defaults={'rating': validated_data.get('rating')}
        )
        return rating




