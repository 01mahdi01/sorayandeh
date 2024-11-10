from django.urls import path
from .apis import RegisterSchool, UpdateSchool, DeleteSchool, LoginSchool

urlpatterns = [
    path('register/', RegisterSchool.as_view(),name="register"),
    path('update_school/', UpdateSchool.as_view(),name="update_school"),
    path('delete_school/', DeleteSchool.as_view(),name="delete_school"),
    path('login_school/', LoginSchool.as_view(),name="login_school"),

]
