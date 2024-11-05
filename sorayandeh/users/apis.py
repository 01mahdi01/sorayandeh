from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from django.core.validators import MinLengthValidator
from .validators import number_validator, special_char_validator, letter_validator, validate_phone_number
from sorayandeh.users.models import BaseUser, Profile
from sorayandeh.api.mixins import ApiAuthMixin
from sorayandeh.users.selectors import get_profile
from sorayandeh.users.services import register, update_user, update_password, update_profile
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema, OpenApiTypes, OpenApiExample
import json

class RegisterApi(APIView):
    """
    API view for registering a new user. Handles both company and personal user registration.
    """

    class CompanyInfoSerializer(serializers.Serializer):
        """
        Serializer for company-specific information.
        """
        employee_name = serializers.CharField(max_length=255)
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

    @extend_schema(
        request=InputRegisterSerializer,
        responses=OutPutRegisterSerializer,
        examples=[
            OpenApiExample(
                "Company Registration Example",
                value={
                    "email": "company@example.com",
                    "name": "Company Name",
                    "phone": "09123456789",
                    "is_company": True,
                    "info": {
                        "employee_name": "Example Corp",
                        "registration_number": "123456789",
                        "address": "123 Example Street"
                    },
                    "password": "SecurePass123!",
                    "confirm_password": "SecurePass123!"
                },
            ),
            OpenApiExample(
                "Person Registration Example",
                value={
                    "email": "person@example.com",
                    "name": "John Doe",
                    "phone": "09123456789",
                    "is_company": False,
                    "info": {
                        "first_name": "John",
                        "last_name": "Doe",
                        "date_of_birth": "1990-01-01"
                    },
                    "password": "SecurePass123!",
                    "confirm_password": "SecurePass123!"
                },
            ),
        ]
    )
    def post(self, request):
        """
        Handle user registration via POST request.
        """
        serializer = self.InputRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            info_str = request.data.get('info', '{}')
            info = json.loads(info_str)  # Convert JSON string to dictionary
        except json.JSONDecodeError:
            return Response({"info": ["Value must be valid JSON."]}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = register(
                email=serializer.validated_data.get("email"),
                password=serializer.validated_data.get("password"),
                info=info,
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
    API view to handle updating user information.

    This view allows authenticated users to update specific fields in their profile,
    including `email`, `name`, `phone`, `is_company`, `info`, and `password`. The
    user only needs to provide the fields they wish to update; unspecified fields
    will remain unchanged.

    Attributes:
        InputUpdateUserSerializer (Serializer): Serializer to validate input data.
    """

    class InputUpdateUserSerializer(serializers.Serializer):
        """
        Serializer for validating input data for updating user fields.

        Fields:
            email (EmailField): Optional; The new email address.
            name (CharField): Optional; The user's new name.
            phone (CharField): Optional; The new phone number, validated by `validate_phone_number`.
            is_company (BooleanField): Optional; Boolean indicating if the user is a company.
            info (JSONField): Optional; A JSON object with user-specific details.

        """

        email = serializers.EmailField(max_length=255, required=False)
        name = serializers.CharField(max_length=255, required=False)
        phone = serializers.CharField(max_length=11, validators=[validate_phone_number], required=False)
        is_company = serializers.BooleanField(required=False)
        info = serializers.JSONField(required=False)


        def validate_email(self, email):
            """
            Validate that the provided email is unique.

            Args:
                email (str): The new email to be validated.

            Raises:
                ValidationError: If the email is already taken by another user.

            Returns:
                str: The validated email.
            """
            if BaseUser.objects.filter(email=email).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError("Email already taken")
            return email

        def validate(self, data):
            """
            data conforms to either company or individual requirements.

            Args:
                data (dict): The input data to be validated.

            Raises:

                if `info` data does not pass validation.

            Returns:
                dict: The validated data.
            """


            # Validate `info` based on `is_company`
            is_company = data.get("is_company", self.instance.is_company)  # fallback to existing value
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
        Handle PUT requests to update user's information.

        This method updates specific fields for the authenticated user.
        Only provided fields will be updated, allowing for partial updates.

        Args:
            request (Request): The HTTP request object containing user input data.

        Returns:
            Response: JSON response containing a success message on successful update,
            or an error message on failure with a 400 status code.
        """
        user_id = request.user.id
        serializer = self.InputUpdateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Extract validated fields to update the user
        update_fields = {key: value for key, value in serializer.validated_data.items() if value is not None}

        try:
            user = update_user(user_id=user_id, **update_fields)
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

            return data

    @extend_schema(request=InputUpdatePasswordSerializer)
    def put(self, request):
        """
        Handle password update via PUT request.
        """
        user_id = request.user.id
        print(request.data)
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





class LoginApi(APIView):
    """
LoginApi:
API view for user login. Accepts email and password, and returns access and refresh tokens if the user is authenticated.
Endpoints:
    POST - Log in a user using email and password. On success, returns JWT tokens and basic user info.

InputLoginSerializer:
    Handles input data validation for login, including:
        - email: User's email address
        - password: User's password

OutputLoginSerializer:
    Defines the output data format, returning:
        - access: JWT access token
        - refresh: JWT refresh token
        - user_id: The authenticated user's ID
        - email: The authenticated user's email address
"""

    class InputLoginSerializer(serializers.Serializer):
        """
        Serializer for login input data.
        """
        email = serializers.EmailField(max_length=255)
        password = serializers.CharField(max_length=128, write_only=True)

    class OutputLoginSerializer(serializers.Serializer):
        """
        Serializer for login output data.
        """
        access = serializers.CharField()
        refresh = serializers.CharField()
        user_id = serializers.IntegerField()
        email = serializers.EmailField()

    @extend_schema(request=InputLoginSerializer, responses=OutputLoginSerializer)
    def post(self, request):
        """
        Handle POST request for user login.
        """
        serializer = self.InputLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Authenticate the user
        user = authenticate(
            request,
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"]
        )

        if user is not None:
            # Generate tokens for the authenticated user
            refresh = RefreshToken.for_user(user)
            data = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user_id": user.id,
                "email": user.email
            }
            return Response(self.OutputLoginSerializer(data).data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"detail": "Invalid credentials. Please try again."},
                status=status.HTTP_401_UNAUTHORIZED
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




class UpdateProfile(APIView):
    """
    API view to handle profile updates for the authenticated user.

    This view allows users to update specific fields in their profile, such as
    `donations` and `campaigns_participated_count`, without requiring all fields
    to be provided in the request. Only the fields sent by the user will be updated.

    Attributes:
        InputUpdateProfileSerializer (Serializer): Serializer to validate input data.
        OutputUpdateProfileSerializer (ModelSerializer): Serializer to format output data.

    Methods:
        put(request): Handles the update request for the user's profile.
    """

    class InputUpdateProfileSerializer(serializers.Serializer):
        """
        Serializer for handling partial updates to the Profile model.

        Fields:
            donations (JSONField): Optional; A dictionary containing donation details.
            campaigns_participated_count (IntegerField): Optional; An integer representing
                the number of campaigns the user has participated in.
        """
        donations = serializers.JSONField(required=False)
        campaigns_participated_count = serializers.IntegerField(required=False)

    class OutputUpdateProfileSerializer(serializers.ModelSerializer):
        """
        Serializer for formatting the Profile model's data in the response.

        Meta:
            model (Profile): The model to be serialized.
            fields (str): Fields to include in the response; all fields are included.
        """
        class Meta:
            model = Profile
            fields = "__all__"

    @extend_schema(responses=OutputUpdateProfileSerializer, request=InputUpdateProfileSerializer)
    def put(self, request):
        """
        Handle PUT requests to update the user's profile.

        This method allows the user to update only the fields they provide in the request.
        If the update is successful, it returns the updated profile data.

        Args:
            request (Request): The request object containing the update data.

        Returns:
            Response: A response object containing the serialized updated profile data
                with a 200 status code, or an error message with a 400 status code.
        """
        user = request.user
        data = request.data

        # Filter out None values and keep only provided fields
        update_fields = {field: value for field, value in data.items() if value is not None}

        try:
            profile = update_profile(user=user, **update_fields)
            return Response(self.OutputUpdateProfileSerializer(profile).data, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response(
                f"Database Error {ex}",
                status=status.HTTP_400_BAD_REQUEST
            )
