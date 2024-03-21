from django.urls import include, path
from rest_framework import routers
from .views import GoogleLogin, GoogleSignup
from . import views

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("google/login", GoogleLogin.as_view(), name="google_login"),
    path("google/signup", GoogleSignup.as_view(), name="google_signup"),
]
