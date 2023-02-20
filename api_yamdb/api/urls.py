
from api.views import CreateUserAPIView, SelfUserPageViewSet, TokenView
from django.urls import path


urlpatterns = [
    path('v1/auth/token/', TokenView.as_view(),),
    path('v1/auth/signup/', CreateUserAPIView.as_view()),
    path('v1/users/me/', SelfUserPageViewSet),
]
