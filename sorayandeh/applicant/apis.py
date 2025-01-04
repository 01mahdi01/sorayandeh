from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from sentry_sdk.integrations.django import is_authenticated

from sorayandeh.applicant.services import register_school, update_school, delete_school
from sorayandeh.applicant.models import School
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from sorayandeh.applicant.validators import JSONSchemaValidator, MY_JSON_FIELD_SCHEMA
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

@permission_classes([AllowAny])
class RegisterSchool(APIView):
    """
    API endpoint to register a new school.

    This API accepts the necessary school information to create a new school and its associated user account. The input is validated and, if valid, the school is created.

    Attributes:
        InputRegisterSchoolSerializer: Serializer to validate and parse input data.
        OutputRegisterSchoolSerializer: Serializer to format the response data.

    Methods:
        post(request):
            Handles the registration process. Accepts JSON input for school details and returns the registered school details.

        Example Input:
            {
                "name": "Green Valley School",
                "postal_code": "12345",
                "school_code_num": "GV123",
                "creator_employee_info": {
                    "employee_name": "John Doe",
                    "employee_phone": "123-456-7890",
                    "employee_position": "Principal"
                },
                "phone": "123456789",
                "email": "admin@school.com",
                "password": "password123",
                "address": "123 Green Valley Road"
            }

        Example Output:
            {
                "postal_code": "12345",
                "school_code_num": "GV123"
            }
    """

    class InputRegisterSchoolSerializer(serializers.Serializer):
        name = serializers.CharField(required=True)
        postal_code = serializers.CharField(required=True)
        school_code_num = serializers.CharField(required=True)
        creator_employee_info = serializers.JSONField(required=True,
                                                      validators=[JSONSchemaValidator(MY_JSON_FIELD_SCHEMA)])
        phone = serializers.CharField(required=True)
        email = serializers.EmailField(required=True)
        password = serializers.CharField(required=True)
        address = serializers.CharField(required=True)

    class OutputRegisterSchoolSerializer(serializers.ModelSerializer):
        class Meta:
            model = School
            fields = ('id','postal_code', 'school_code_num')

    def validate(self, data):
        pass

    @extend_schema(request=InputRegisterSchoolSerializer, responses=OutputRegisterSchoolSerializer)
    def post(self, request):
        serializer = self.InputRegisterSchoolSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # ---------------------here it must become a task to first authenticate the school then create them
        try:
            school = register_school(
                name=serializer.validated_data['name'],
                postal_code=serializer.validated_data['postal_code'],
                school_code_num=serializer.validated_data['school_code_num'],
                creator_employee_info=serializer.validated_data['creator_employee_info'],
                phone=serializer.validated_data['phone'],
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password'],
                address=serializer.validated_data["address"],
            )
            return Response(self.OutputRegisterSchoolSerializer(school, context={"request": request}).data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UpdateSchool(APIView):
    """
    API endpoint to update an existing school.

    This API allows partial updates to the school and its associated user account. The input is validated, and only the provided fields are updated.

    Attributes:
        InputUpdateSchoolSerializer: Serializer to validate and parse input data.
        OutputUpdateSchoolSerializer: Serializer to format the response data.

    Methods:
        put(request):
            Handles the update process. Accepts JSON input with the fields to update and returns the updated school details.

        Example Input:
            {
                "school_code_num": "GV123",
                "postal_code": "54321",
                "address": "456 New Valley Road"
            }

        Example Output:
            {
                "postal_code": "54321",
                "school_code_num": "GV123"
            }
    """

    class InputUpdateSchoolSerializer(serializers.Serializer):
        name = serializers.CharField(required=False)
        postal_code = serializers.CharField(required=False)
        school_code_num = serializers.CharField(required=True)
        creator_employee_info = serializers.JSONField(required=False)
        phone = serializers.CharField(required=False)
        email = serializers.EmailField(required=False)
        password = serializers.CharField(required=False)
        address = serializers.CharField(required=False)

    class OutputUpdateSchoolSerializer(serializers.ModelSerializer):
        class Meta:
            model = School
            fields = ('postal_code', 'school_code_num')

    @extend_schema(request=InputUpdateSchoolSerializer, responses=OutputUpdateSchoolSerializer)
    def put(self, request):
        serializer = self.InputUpdateSchoolSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = request.data
        school_code = data.get('school_code_num')
        update_fields = {field: value for field, value in data.items() if value is not None}
        try:
            updated_school = update_school(school_code=school_code, **update_fields)
            return Response(self.OutputUpdateSchoolSerializer(updated_school, context={"request": request}).data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DeleteSchool(APIView):
    """
    API endpoint to delete a school.

    This API is used to remove a school from the system. Deleting a school will also remove its associated user account.

    Attributes:
        InputDeleteSchoolSerializer: Serializer to validate and parse input data.

    Methods:
        post(request):
            Handles the deletion process. Accepts the name of the school to delete.

        Example Input:
            {
                "name": "Green Valley School"
            }

        Example Output:
            {
                "detail": "School deleted successfully."
            }
    """

    class InputDeleteSchoolSerializer(serializers.Serializer):
        name = serializers.CharField(required=True)

@permission_classes([AllowAny])
class LoginSchool(APIView):
    """
    API endpoint to log in as a school.

    This API accepts school credentials, authenticates the school, and returns a JWT token pair (access and refresh) if authentication is successful.

    Attributes:
        InputLoginSchoolSerializer: Serializer to validate and parse login credentials.
        OutputLoginSchoolSerializer: Serializer to format the login response.

    Methods:
        post(request):
            Handles the login process. Accepts school code and password, and returns JWT tokens on successful authentication.

        Example Input:
            {
                "school_code_num": "GV123",
                "password": "password123"
            }

        Example Output:
            {
                "access": "access_token_here",
                "refresh": "refresh_token_here",
                "user_id": 1,
                "school_code_num": "GV123"
            }

        Notes:
            - Ensure the school code and password are correct.
            - Invalid credentials will result in a 401 Unauthorized response.
    """

    class InputLoginSchoolSerializer(serializers.Serializer):
        school_code_num = serializers.CharField(required=True)
        password = serializers.CharField(required=True)

    class OutputLoginSchoolSerializer(serializers.Serializer):
        access = serializers.CharField()
        refresh = serializers.CharField()
        user_id = serializers.IntegerField()
        school_code_num = serializers.CharField()

    @extend_schema(request=InputLoginSchoolSerializer, responses=OutputLoginSchoolSerializer)
    def post(self, request):
        serializer = self.InputLoginSchoolSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Authenticate the school user
        user = authenticate(
            request,
            school_code_num=serializer.validated_data["school_code_num"],
            password=serializer.validated_data["password"],
        )

        if user is not None and is_authenticated:
            # Generate tokens for the authenticated user
            refresh = RefreshToken.for_user(user)
            data = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user_id": user.id,
                "school_code_num": serializer.validated_data["school_code_num"],
            }
            return Response(self.OutputLoginSchoolSerializer(data).data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"detail": "Invalid credentials. Please try again."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
