from django.db import models
from users.models import User
from enum import Enum

# Create your models here.


class Status(Enum):
    PENDING = "pending"
    DELIVERED = "Delivered"


class Conversation(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # status = models.CharField(max_length=10, choices=Status, default=Status.PENDING)
