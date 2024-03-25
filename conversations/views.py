from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from .serializers import ConversationSerializers, MessageSerializer
from .models import Conversation, Message
from django.shortcuts import get_object_or_404


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializers
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Conversation.objects.filter(user=user)
        return queryset

    def retrieve(self, request, pk=None, *args, **kwargs):
        conversation = get_object_or_404(Conversation, pk=pk)
        if self.request.user != conversation.user:
            return Response(
                {"error": "Not Authorized"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.get_serializer(conversation)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if serializer.validated_data["user"] != self.request.user:
            return Response(
                {"error": "Not Authorized"},
                status=status.HTTP_403_FORBIDDEN,
            )

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
