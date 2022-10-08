from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as rest_filters
from rest_framework import (filters, pagination, viewsets, status,
                            permissions)
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from api import mixins
from reviews.models import Review
from titles.models import Category, Genre, Title
from users.models import CustomUser
from api.filters import TitleFilter
from api.permissions import (IsAdminModeratorAuthorOrReadOnly,
                             IsAdminOrReadOnly, IsAdmin)
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             TitleReadSerializer, TitleWriteSerializer,
                             NewUserSerializer, TokenGenerationSerializer,
                             UserSerializer)


class CategoryViewSet(mixins.CreateListDestroyViewSet):
    """Получение списка категорий, создание и удаление категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    pagination_class = pagination.PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)


class GenreViewSet(mixins.CreateListDestroyViewSet):
    """Получение списка жанров, создание и удаление жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    pagination_class = pagination.PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    """Все СRUD-операции с произведениями."""
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score'))
    serializer_class = TitleWriteSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    pagination_class = pagination.LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Все СRUD-операции с отзывами."""
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Все СRUD-операции с комментариями."""
    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


token_generator = PasswordResetTokenGenerator()


class NewUserView(APIView):
    """Регистрация пользователей."""
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        """
        Получение от пользователя имени и электронной почты.
        Генерация кода подтверждения и отправка его на почтовый адрес.
        Сохранение неактивной учетной записи в БД.
        """
        serializer = NewUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        user, created = CustomUser.objects.get_or_create(
            username=username,
            email=email
        )
        confirmation_code = token_generator.make_token(user)
        message = f'Ваш код подтверждения: {confirmation_code}'
        if created:
            user.is_active = False
            user.save()
        send_mail(
            subject='Код подтверждения',
            message=message,
            from_email=settings.EMAIL_FROM,
            recipient_list=(email,)
        )
        context = {
            'username': username,
            'email': email
        }
        return Response(context, status=status.HTTP_200_OK)


class GetTokenView(APIView):
    """Получение токена."""
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = TokenGenerationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = serializer.validated_data.get('confirmation_code')
        username = serializer.validated_data.get('username')
        user = get_object_or_404(CustomUser, username=username)
        if token_generator.check_token(user, confirmation_code):
            user.is_active = True
            user.save()
            token = AccessToken.for_user(user)
            return Response({'token': f'{token}'}, status=status.HTTP_200_OK)
        return Response(
            {'confirmation_code': 'Код не действителен.'},
            status=status.HTTP_400_BAD_REQUEST
        )


class UserViewSet(viewsets.ModelViewSet):
    """Все СRUD-операции с пользователями для админа."""
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (rest_filters.DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('=username',)
    lookup_field = 'username'

    @action(
        detail=False,
        methods=('GET', 'PATCH'),
        permission_classes=(permissions.IsAuthenticated,)
    )
    def me(self, request):
        """Частичное обновление своего профиля."""
        user = self.request.user
        serializer = self.get_serializer(user)
        if self.request.method == 'PATCH':
            serializer = self.get_serializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=user.role)
        return Response(serializer.data)
