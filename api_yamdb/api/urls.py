from django.urls import include, path

from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       GetTokenView, NewUserView, ReviewViewSet,
                       TitleViewSet, UserViewSet)
from rest_framework.routers import DefaultRouter

app_name = 'api'

router = DefaultRouter()
router.register(
    'users',
    UserViewSet,
    basename='users')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                r'/comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', NewUserView.as_view(), name='signup'),
    path('v1/auth/token/', GetTokenView.as_view(), name='token'),
]
