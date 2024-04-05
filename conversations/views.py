import time
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from .serializers import ConversationSerializers, MessageSerializer
from .models import Conversation, Message
from django.http import StreamingHttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .services import chatService


conversation_create_schema={
    'description': 'create conversation view ',
    'auth': None,
    'request': {
        "application/json": {
            "properties": {
                "title": {
                    "type": "string",
                },
            },
            "required": [
                "title",
            ]
        }
    },
}

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializers
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = [
        "post",
        "get",
    ]

    def retrieve(self, request, pk=None, *args, **kwargs):
        conversation = get_object_or_404(Conversation, pk=pk)
        if self.request.user != conversation.user:
            return Response(
                {"error": "Not Authorized"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.get_serializer(conversation)
        return Response(serializer.data)
    
    @extend_schema(**conversation_create_schema)

    def create(self, request, *args, **kwargs):
        request.data["user"] = request.user.pk
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

message_create_schema={
    'description': 'create conversation view ',
    'auth': None,
    'request': {
        "application/json": {
            "properties": {
                "conversation": {
                    "type": "number",
                },
                "content":{
                    "type":"string"
                }
            },
            "required": [
                "conversation","content"
            ]
        }
    }, 
}
class MessagesViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = [
        "post",
        "get",
    ]

    def stream_response_generator(self):
        constant_string = """Description:
HRGPT is a comprehensive software solution designed to streamline human resources processes and enhance performance tracking within an organization. It provides a centralized platform for HR personnel and managers to manage employee data, track performance metrics, and facilitate communication and collaboration across teams.
Key Features:
Employee Database: HRGPT maintains a database of employee information, including personal details, employment history, and contact information.
Performance Management: The system allows managers to set goals, conduct performance evaluations, and provide feedback to employees.
Training and Development: HRGPT facilitates employee training and development by tracking training courses, certifications, and skill development initiatives.
Recruitment and Onboarding: The platform streamlines the recruitment process by posting job vacancies, managing applications, and conducting onboarding procedures for new hires.
Leave and Attendance Management: Employees can request leave, and managers can approve or reject leave requests. The system also tracks attendance records.
Compensation and Benefits: HRGPT manages employee compensation, benefits, and payroll information, ensuring accuracy and compliance with company policies and regulations.
Communication and Collaboration: The platform includes features for internal communication, such as messaging, announcements, and document sharing, to foster collaboration among employees.
Reporting and Analytics: HRGPT generates reports and analytics on various HR metrics, such as employee performance, turnover rates, and workforce demographics, to support data-driven decision-making.
Security and Compliance: The system prioritizes data security and compliance with relevant regulations, such as GDPR (General Data Protection Regulation) or local labor laws, to protect employee privacy and sensitive information."""
        chunk_size = 100
        delay_seconds = 1
        for i in range(0, len(constant_string), chunk_size):
            yield constant_string[i : i + chunk_size]
            time.sleep(delay_seconds)
            
    
    @extend_schema(**message_create_schema)

    def create(self, request, conversation_pk=None, *args, **kwargs):
        request.data["type"] = Message.SEND
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversation = get_object_or_404(Conversation, pk=request.data["conversation"])
        if request.user != conversation.user:
            return Response(
                {"error": "Not Authorized"},
                status=status.HTTP_403_FORBIDDEN,
            )
        self.perform_create(serializer)
        response = chatService(serializer.validated_data["content"])
        message_data = {
            "content": response["data"],
            "conversation": request.data["conversation"],
            "type":Message.RECEIVED
        }
        message_serializer = self.serializer_class(data=message_data)
        message_serializer.is_valid(raise_exception=True)
        message_serializer.save()
        return Response(message_serializer.data["content"], status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        message_obj = Message.objects.filter(
            conversation__id=kwargs.get("pk"), conversation__user=request.user
        )
        message_obj_serializer = MessageSerializer(message_obj, many=True)
        return Response(message_obj_serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_messages_list(request, *args, **kwargs):
    conversations = Conversation.objects.filter(user=request.user)
    all_messages = []
    for conversation in conversations:
        message = (
            Message.objects.filter(conversation=conversation)
            .order_by("created_at")
            .first()
        )
        if message:
            message_data = MessageSerializer(message).data
            all_messages.append(message_data)
    return Response(all_messages)
