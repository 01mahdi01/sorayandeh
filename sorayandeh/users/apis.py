from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers

from django.core.validators import MinLengthValidator
from .validators import number_validator, special_char_validator, letter_validator, validate_phone_number
from sorayandeh.users.models import BaseUser , Profile
from sorayandeh.api.mixins import ApiAuthMixin
from sorayandeh.users.selectors import get_profile
from sorayandeh.users.services import register ,update_user, update_password
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from drf_spectacular.utils import extend_schema


class RegisterApi(APIView):
    """
    API view for registering a new user. Handles both company and personal user registration.
    """

    class CompanyInfoSerializer(serializers.Serializer):
        """
        Serializer for company-specific information.
        """
        company_name = serializers.CharField(max_length=255)
        registration_number = serializers.CharField(max_length=100)
        address = serializers.CharField(max_length=500)

    class PersonInfoSerializer(serializers.Serializer):
        """
        Serializer for personal-specific information.
        """
        first_name = serializers.CharField(max_length=100)
        last_name = serializers.CharField(max_length=100)
        date_of_birth = serializers.DateField()

    class InputRegisterSerializer(serializers.Serializer):
        """
        Serializer for input data during user registration.
        """
        email = serializers.EmailField(max_length=255)
        name = serializers.CharField(max_length=255)
        phone = serializers.CharField(max_length=11, validators=[validate_phone_number])
        is_company = serializers.BooleanField()
        info = serializers.JSONField()
        password = serializers.CharField(
            validators=[
                number_validator,
                letter_validator,
                special_char_validator,
                MinLengthValidator(limit_value=10)
            ]
        )
        confirm_password = serializers.CharField(max_length=255)

        def validate_email(self, email):
            """
            Validate that the email is unique.
            """
            if BaseUser.objects.filter(email=email).exists():
                raise serializers.ValidationError("email Already Taken")
            return email

        def validate(self, data):
            """
            Validate password and ensure `info` field is correctly formatted.
            """
            if not data.get("password") or not data.get("confirm_password"):
                raise serializers.ValidationError("Please fill password and confirm password")

            if data.get("password") != data.get("confirm_password"):
                raise serializers.ValidationError("confirm password is not equal to password")

            is_company = data.get("is_company")
            info_data = data.get("info")

            if is_company:
                info_serializer = RegisterApi.CompanyInfoSerializer(data=info_data)
            else:
                info_serializer = RegisterApi.PersonInfoSerializer(data=info_data)

            info_serializer.is_valid(raise_exception=True)
            data['info'] = info_serializer.validated_data
            return data

    class OutPutRegisterSerializer(serializers.ModelSerializer):
        """
        Serializer for the output data after user registration.
        """
        token = serializers.SerializerMethodField("get_token")

        class Meta:
            model = BaseUser
            fields = ("email", "token", "created_at", "updated_at")

        def get_token(self, user):
            """
            Generate tokens for user authentication.
            """
            data = dict()
            token_class = RefreshToken

            refresh = token_class.for_user(user)

            data["refresh"] = str(refresh)
            data["access"] = str(refresh.access_token)

            return data

    @extend_schema(request=InputRegisterSerializer, responses=OutPutRegisterSerializer)
    def post(self, request):
        """
        Handle user registration via POST request.
        """
        serializer = self.InputRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = register(
                email=serializer.validated_data.get("email"),
                password=serializer.validated_data.get("password"),
                info=serializer.validated_data.get("info"),
                phone=serializer.validated_data.get("phone"),
                name=serializer.validated_data.get("name"),
                is_company=serializer.validated_data.get("is_company"),
            )
        except Exception as ex:
            return Response(
                f"Database Error {ex}",
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(self.OutPutRegisterSerializer(user, context={"request": request}).data)


class UpdateUser(APIView):
    """
    API view for updating user information.
    """

    class InputUpdateUserSerializer(serializers.Serializer):
        """
        Serializer for input data during user information update.
        """
        email = serializers.EmailField(max_length=255, required=False)
        name = serializers.CharField(max_length=255, required=False)
        phone = serializers.CharField(max_length=11, validators=[validate_phone_number], required=False)
        is_company = serializers.BooleanField(required=False)
        info = serializers.JSONField(required=False)
        password = serializers.CharField(
            validators=[
                number_validator,
                letter_validator,
                special_char_validator,
                MinLengthValidator(limit_value=10)
            ],
            required=False
        )
        confirm_password = serializers.CharField(max_length=255, required=False)

        def validate_email(self, email):
            """
            Validate that the email is unique, excluding the current user.
            """
            if BaseUser.objects.filter(email=email).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError("Email already taken")
            return email

        def validate(self, data):
            """
            Validate password and ensure `info` field is correctly formatted.
            """
            if "password" in data or "confirm_password" in data:
                if data.get("password") != data.get("confirm_password"):
                    raise serializers.ValidationError("Confirm password does not match password")

            is_company = data.get("is_company", self.instance.is_company)
            info_data = data.get("info", self.instance.info)

            if is_company:
                info_serializer = RegisterApi.CompanyInfoSerializer(data=info_data)
            else:
                info_serializer = RegisterApi.PersonInfoSerializer(data=info_data)

            info_serializer.is_valid(raise_exception=True)
            data['info'] = info_serializer.validated_data
            return data

    @extend_schema(request=InputUpdateUserSerializer)
    def put(self, request):
        """
        Handle user information update via PUT request.
        """
        user_id = request.user.id
        serializer = self.InputUpdateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = update_user(
                user_id=user_id,
                email=serializer.validated_data.get("email"),
                info=serializer.validated_data.get("info"),
                phone=serializer.validated_data.get("phone"),
                name=serializer.validated_data.get("name"),
            )
            return Response({"message": "User updated successfully"}, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response(
                f"Database Error {ex}",
                status=status.HTTP_400_BAD_REQUEST
            )


class UpdatePassword(APIView):
    """
    API view for updating user password.
    """

    class InputUpdatePasswordSerializer(serializers.Serializer):
        """
        Serializer for input data during password update.
        """
        password = serializers.CharField(
            validators=[
                number_validator,
                special_char_validator,
                MinLengthValidator(limit_value=10)
            ]
        )
        confirm_password = serializers.CharField(max_length=255, required=False)

        def validate(self, data):
            """
            Validate that password and confirm_password match.
            """
            if not data.get("password") or not data.get("confirm_password"):
                raise serializers.ValidationError("Please fill password and confirm password")

            if data.get("password") != data.get("confirm_password"):
                raise serializers.ValidationError("confirm password is not equal to password")

    @extend_schema(request=InputUpdatePasswordSerializer)
    def put(self, request):
        """
        Handle password update via PUT request.
        """
        user_id = request.user.id
        serializer = self.InputUpdatePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = update_password(
                user_id=user_id,
                password=serializer.validated_data.get("password"),
            )

            return Response({"message": "Password changed and sessions expired. Please log in again."},
                            status=status.HTTP_200_OK)
        except Exception as ex:
            return Response(
                f"Database Error {ex}",
                status=status.HTTP_400_BAD_REQUEST
            )


class ProfileApi(ApiAuthMixin, APIView):
    """
    API view for retrieving user profile information.
    """

    class OutPutSerializer(serializers.ModelSerializer):
        """
        Serializer for output profile data.
        """

        class Meta:
            model = Profile
            fields = ("donations", "campaigns_participated_count")

    @extend_schema(responses=OutPutSerializer)
    def get(self, request):
        """
        Handle GET request to retrieve user profile.
        """
        query = get_profile(user=request.user)
        return Response(self.OutPutSerializer(query, context={"request": request}).data)
