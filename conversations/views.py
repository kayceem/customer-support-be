import time
from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from .serializers import ConversationSerializers, MessageSerializer
from .models import Conversation, Message
from django.http import StreamingHttpResponse

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

    def list(self, request, *args, **kwargs):
        query_set = self.get_queryset()
        serializer = self.get_serializer(query_set, many=True)
        return Response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    # permission_classes = [permissions.IsAuthenticated]

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

    def create(self, request, conversation_pk=None, *args, **kwargs):
        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)

        # conversation = get_object_or_404(Conversation, pk=conversation_pk)

        # request_body_user = serializer.validated_data["user"]
        # if (
        #     request_body_user != self.request.user
        #     or conversation.user != self.request.user
        # ):
        #     return Response(
        #         {"error": "Not Authorized"},
        #         status=status.HTTP_403_FORBIDDEN,
        #     )
        # self.perform_create(serializer)
        # client = chat_service.OpenAIService()
        # completion_generator = client.generate_completion(
        #     serializer.validated_data["content"]
        # )

        response = StreamingHttpResponse(
            self.stream_response_generator(),
            status=200,
            content_type="text/event-stream",
        )
        response["Cache-Control"] = "no-cache"
        return response

    def retrieve(self, request, pk=None, conversation_pk=None):
        conversation = get_object_or_404(Conversation, pk=conversation_pk)
        if self.request.user != conversation.user:
            return Response(
                {"error": "Not Authorized"},
                status=status.HTTP_403_FORBIDDEN,
            )

        message = get_object_or_404(Message, pk=pk)
        if conversation != message.conversation:
            return Response(
                {"error": "Bad Request"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(message)
        return Response(serializer.data)
