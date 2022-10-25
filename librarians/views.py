import ipdb
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView, Request, Response, status
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import CustomJWTSerializer, LoginSerializer, RegisterSerializer


class RegisterView(APIView):
    def post(self, request: Request) -> Response:
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


class LoginJWTView(TokenObtainPairView):
    serializer_class = CustomJWTSerializer


# class LoginView(ObtainAuthToken):
#     ...
# def post(self, request: Request) -> Response:
#     serializer = self.serializer_class(
#         data=request.data, context={"request": request}
#     )

#     serializer.is_valid(raise_exception=True)
#     # ipdb.set_trace()

#     user = serializer.validated_data["user"]
#     token, _ = Token.objects.get_or_create(user=user)

#     return Response({"token": token.key})


# Maneira Manual
class LoginViewOld(APIView):
    def post(self, request: Request) -> Response:
        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )

        if not user:
            return Response(
                {"detail": "invalid credentials"}, status.HTTP_400_BAD_REQUEST
            )

        # Equivalentes
        # token, created = Token.objects.get_or_create(user=user)
        token, _ = Token.objects.get_or_create(user=user)

        return Response({"token": token.key})

        # user = authenticate(**serializer.validated_data)
