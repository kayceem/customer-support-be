from .models import Conversation, Message
from rest_framework import serializers


class ConversationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ["id", "user", "created_at"]
        read_only_fields = ["id", "created_at"]


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "conversation", "content", "created_at"]
        read_only_fields = ["id", "created_at"]
