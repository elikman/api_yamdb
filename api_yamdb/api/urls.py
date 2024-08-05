from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views

from api.views import (CategoryViewSet, CommentViewSet, CreateTokenView,
                       GenreViewSet, ReviewViewSet, SignupView, TitleViewSet,
                       UserViewSet)

router = routers.DefaultRouter()
router.register("categories", CategoryViewSet, basename="categories")
router.register("genres", GenreViewSet, basename="genres")
router.register("titles", TitleViewSet, basename="titles")
router.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="review"
)
router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comment",
)
router.register(r"users", UserViewSet, basename="user")

auth_urls = [
    path("signup/", SignupView.as_view(), name="user-signup"),
    path("token/", CreateTokenView.as_view(), name="token-generation"),
]

v1_urls = [
    path("", include(router.urls)),
    path("auth/", include(auth_urls)),
    path("api-token-auth/", views.obtain_auth_token),
]

urlpatterns = [
    path("v1/", include(v1_urls)),
]
