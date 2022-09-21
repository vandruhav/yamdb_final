"""Эндпойнты приложения 'api'."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoriesViewSet, CommentsViewSet, GenresViewSet,
                    ReviewViewSet, TitleViewSet, UserViewSet, register_view,
                    token_view)

app_name = "api"

router = DefaultRouter()
router.register(r"users", UserViewSet, basename='users')
router.register(r'categories', CategoriesViewSet, basename='categories')
router.register(r'genres', GenresViewSet, basename='genres')
router.register(r'titles', TitleViewSet, basename='titles')
router.register(
    r'titles/(?P<url_title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<url_title_id>\d+)/reviews/(?P<url_review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments'
)

auth_urlpatterns = [
    path('signup/', register_view),
    path(
        'token/',
        token_view,
        name='token_obtain_pair'
    ),
]

urlpatterns = [
    path("v1/auth/", include(auth_urlpatterns)),
    path("v1/", include(router.urls)),
]
