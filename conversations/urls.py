from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ConversationViewSet,
    MessagesViewSet,
    get_messages_list,
)

router = DefaultRouter()
router.register(
    "chat",
    MessagesViewSet,
)
router.register("", ConversationViewSet)
urlpatterns = [
    path("", include(router.urls)),
    path("messages/list", get_messages_list, name="get_messages_list"),
]
