from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

from django.conf import settings
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework import filters, permissions, status, viewsets
from rest_framework.response import Response
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

from .serializers import UserSerializer
from .models import User


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.REDIRECT_URL
    client_class = OAuth2Client

    def finalize_response(self, request, response, *args, **kwargs):
        if self.user is None:
            error_response = {"error": "Couldn't login with Google Login"}
            response = Response(error_response, status=status.HTTP_404_NOT_FOUND)
            return super().finalize_response(request, response, *args, **kwargs)
        user_exists = self.user_exists()

        if not user_exists:
            error_response = {"error": "User not registered with this social account."}
            response = Response(error_response, status=status.HTTP_404_NOT_FOUND)
            return super().finalize_response(request, response, *args, **kwargs)
        return super().finalize_response(request, response, *args, **kwargs)

    def user_exists(self):
        return self.user.is_registered


class GoogleSignup(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.REDIRECT_URL
    client_class = OAuth2Client

    def finalize_response(self, request, response, *args, **kwargs):
        user_exists = self.user_exists()
        if user_exists:
            error_response = {"error": "User already exists"}
            response = Response(
                error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            return super().finalize_response(request, response, *args, **kwargs)

        self.user.is_registered = True
        self.user.save()

        return super().finalize_response(request, response, *args, **kwargs)

    def user_exists(self):
        return self.user.is_registered


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
