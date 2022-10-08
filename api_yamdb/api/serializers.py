from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from users.models import CustomUser
from reviews.models import Comment, Review
from titles.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    class Meta:
        model = Category
        exclude = ('id',)
        slug_field = ('slug',)


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""

    class Meta:
        model = Genre
        exclude = ('id',)
        slug_field = ('slug',)


class TitleReadSerializer(serializers.ModelSerializer):
    """
    Сериализатор для произведений.
    Операции с чтением.
    """
    genre = GenreSerializer(many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category')


class TitleWriteSerializer(serializers.ModelSerializer):
    """
    Сериализатор для произведений.
    Операции с записью.
    """
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True)
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    def validate(self, data):
        """Проверка корректности вводимой даты."""
        if (self.context['request'].method == 'POST'
                and data['year'] > timezone.now().year):
            raise serializers.ValidationError('Выберите корректный год!')
        return data

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов."""
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    def validate(self, data):
        """
        Проверка на то, что пользователь уже оставлял отзыв на произведение.
        Предусмотрена возможность оставить только один отзыв.
        """
        author = self.context.get('request').user
        title = get_object_or_404(
            Title, pk=self.context['view'].kwargs.get('title_id'))
        if self.context.get('request').method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise serializers.ValidationError('Вы можете оставить только'
                                                  'один отзыв на произведение!'
                                                  )
        return data

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев."""
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели CustomUser."""

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        ]


class NewUserSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователей."""

    username = serializers.CharField(
        validators=[UniqueValidator(queryset=CustomUser.objects.all(),
                                    message='Пользователь с таким именем '
                                            'уже существует!')]
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=CustomUser.objects.all(),
                                    message='Пользователь с таким адресом '
                                            'электронной почты '
                                            'уже существует')]
    )

    def validate_username(self, value):
        """
        Проверка на уровне поля username.
        ME нельзя использовать в качестве username.
        """
        valid_values = ('me', 'ME', 'mE', 'Me')
        if value in valid_values:
            raise ValidationError(
                'Использовать имя "me" в качестве '
                'username запрещено.'
            )
        return value

    class Meta:
        model = CustomUser
        fields = ['username', 'email']


class TokenGenerationSerializer(serializers.ModelSerializer):
    """Сериализатор для генерации токена."""
    username = serializers.CharField()
    confirmation_code = serializers.CharField(max_length=100)

    class Meta:
        model = CustomUser
        fields = ['username', 'confirmation_code']
