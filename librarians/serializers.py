import ipdb
from rest_framework import serializers
from rest_framework.exceptions import APIException
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Librarian, ShiftOptions


class UniqueValidationError(APIException):
    status_code = 422


class RegisterSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField()
    # username = serializers.CharField(
    #     validators=[UniqueValidator(queryset=Librarian.objects.all())]
    # )
    shift = serializers.CharField(
        allow_blank=True, allow_null=True, default=ShiftOptions.DEFAULT
    )
    ssn = serializers.IntegerField()
    birthdate = serializers.DateField()
    is_superuser = serializers.BooleanField(read_only=True)
    password = serializers.CharField(write_only=True)

    def validate_ssn(self, value: int):
        if Librarian.objects.filter(ssn=value).exists():
            # raise serializers.ValidationError("ssn already registered")
            raise UniqueValidationError("ssn already registered")

        return value

    def validate_username(self, value: str):
        if Librarian.objects.filter(username=value).exists():
            raise UniqueValidationError("username already registered")

        return value

    def create(self, validated_data):
        # import ipdb

        # ipdb.set_trace()
        return Librarian.objects.create_user(**validated_data)


class CustomJWTSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, librarian: Librarian):
        # ipdb.set_trace()
        token = super().get_token(librarian)
        token["ssn"] = librarian.ssn
        return token


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
