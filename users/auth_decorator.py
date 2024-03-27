from rest_framework.response import Response
from rest_framework import status
import firebase_admin
from firebase_admin import credentials, auth

cred = credentials.Certificate("./serviceAccountKey.json")
firebase_app = firebase_admin.initialize_app(cred)


def firebase_authenticate():
    def decorator(func):
        def wrapper(args, **kwargs):
            request = args[-1]
            token = request.data.get("token", None)

            if not token:
                return Response(
                    {"success": False, "data": "No Auth Token"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                decoded_token = auth.verify_id_token(token)
                request.data["decoded_token"] = decoded_token

            except auth.ExpiredIdTokenError:

                print("Login Token Expired")
                return Response(
                    {
                        "success": False,
                        "token_expired": True,
                        "data": "Login Token Expired",
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            except Exception as err:
                return Response(
                    {"success": False, "token_invalid": True, "data": "Invalid Token"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            return func(args, **kwargs)

        return wrapper

    return decorator
