from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import Login

router = DefaultRouter()
router.register("login", Login)
urlpatterns = [
    path("", include(router.urls)),
]
