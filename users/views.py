from rest_framework import filters, permissions, status, viewsets
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .auth_decorator import firebase_authenticate
from .serializers import UserSerializer
from .services import User as userServices
from .models import User


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        return Response(
            {"detail": "User creation is not allowed through this endpoint."},
            status=status.HTTP_403_FORBIDDEN,
        )


view_schema = {
    'description': 'login view ',
    'auth': None,
    'request': {
        "application/json": {
            "properties": {
                "token": {
                    "type": "string",
                },
            },
            "required": [
                "token",
            ]
        }
    },
    'responses': {
        (200, "application/json"): {
            "description": "Success",
            "type": "object",
            "properties": {
                "status": {
                    "type": "boolean"
                },
                "access_token": {
                    "type": "string",
                    "minLength": 1
                },
            },
            "required": [
                "status"
                "access_token",

            ]
        },
        (401, "application/json"): {
            "description": "Login failure",
            "type": "object",
            "properties": {
                "status": {
                    "type": "boolean"
                },
                "error": {
                    "type": "string"
                }
            },
            "required": [
                "status"
            ]
        }
    }
}


class Login(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    http_method_names = [
        "post",
    ]

    @extend_schema(**view_schema)
    @firebase_authenticate()
    def create(self, request):
        decoded_token = request.data.get("decoded_token")
        email = decoded_token["email"]
        name = decoded_token.get("name", "")
        token = userServices.login(email, name)
        return Response(
            {"success": True, "access_token": token}, status=status.HTTP_200_OK
        )
