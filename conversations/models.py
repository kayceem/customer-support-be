from django.db import models
from users.models import User


class Conversation(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    SEND = "Send"
    RECEIVED = "Received"

    CHAT_TYPE = (
        (SEND, SEND),
        (RECEIVED, RECEIVED),
    )
    id = models.AutoField(primary_key=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    content = models.TextField(default=" ", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=10, choices=CHAT_TYPE, default=SEND)
