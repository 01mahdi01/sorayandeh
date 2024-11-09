from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from sorayandeh.applicant.services import register_school, update_school, delete_school
from sorayandeh.applicant.models import School
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken




class RegisterSchool(APIView):
    class EmployeeInfoSerializer(serializers.Serializer):
        employee_name = serializers.CharField(required=True)
        employee_phone = serializers.CharField(required=True)
        employee_position = serializers.CharField(required=True)

    class InputRegisterSchoolSerializer(serializers.Serializer):
        name = serializers.CharField(required=True)
        postal_code = serializers.CharField(required=True)
        school_code_num = serializers.CharField(required=True)
        creator_employee_info = serializers.JSONField(required=True)
        phone = serializers.CharField(required=True)
        email = serializers.EmailField(required=True)
        password = serializers.CharField(required=True)
        address = serializers.CharField(required=True)


    class OutputRegisterSchoolSerializer(serializers.ModelSerializer):
        class Meta:
            model = School
            fields = ('postal_code', 'school_code_num')

    def validate(self, data):
        employee_info = data.get("creator_employee_info")
        employee_phone_serializer = RegisterSchool.EmployeeInfoSerializer(data=employee_info)
        employee_phone_serializer.is_valid(raise_exception=True)
        return data

    @extend_schema(request=InputRegisterSchoolSerializer, responses=OutputRegisterSchoolSerializer)
    def post(self, request):
        serializer = self.InputRegisterSchoolSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        #---------------------here it must become a task to first authenticate the school then create them
        try:
            school = register_school(
                name=serializer.validated_data['name'],
                postal_code=serializer.validated_data['postal_code'],
                school_code_num=serializer.validated_data['school_code_num'],
                creator_employee_info=serializer.validated_data['creator_employee_info'],
                phone=serializer.validated_data['phone'],
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password'],
                address = serializer.validated_data["address"],
            )
            return Response(self.OutputRegisterSchoolSerializer(school, context={"request": request}).data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UpdateSchool(APIView):
    class InputUpdateSchoolSerializer(serializers.Serializer):
        name = serializers.CharField(required=False)
        postal_code = serializers.CharField(required=False)
        school_code_num = serializers.CharField(required=True)

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
    class InputDeleteSchoolSerializer(serializers.Serializer):
        name = serializers.CharField(required=True)


class LoginSchool(APIView):
    class InputLoginSchoolSerializer(serializers.Serializer):
        school_code_num=serializers.CharField(required=True)
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

        if user is not None:
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

