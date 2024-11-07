from django.urls import path
from .apis import RegisterSchool, UpdateSchool, DeleteSchool

urlpatterns = [
    path('register/', RegisterSchool.as_view(),name="register"),
    path('update_school/', UpdateSchool.as_view(),name="update_school"),
    path('delete_school/', DeleteSchool.as_view(),name="delete_school"),

]
