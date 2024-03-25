from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet

router = DefaultRouter()
router.register("chat", MessageViewSet)
router.register("", ConversationViewSet)
urlpatterns = [
    path("", include(router.urls)),
]
