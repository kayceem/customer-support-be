from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessagesViewSet

router = DefaultRouter()
router.register(
    "chat",
    MessagesViewSet,
)
router.register("", ConversationViewSet)
urlpatterns = [
    path("", include(router.urls)),
]
