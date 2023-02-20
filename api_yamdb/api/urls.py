from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    ReviewViewSet, CommentViewSet,
    TitleViewSet, GenreViewSet, CategoriesViewSet
)
from api.views import CreateUserAPIView, SelfUserPageViewSet, TokenView


app_name = 'api'

router = DefaultRouter()
router.register('titles', TitleViewSet)
router.register('genres', GenreViewSet)
router.register('categories', CategoriesViewSet)
router.register(
    r'^titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review'
)
router.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/token/', TokenView.as_view(),),
    path('v1/auth/signup/', CreateUserAPIView.as_view()),
    path('v1/users/me/', SelfUserPageViewSet),
]
