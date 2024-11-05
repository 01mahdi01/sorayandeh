from django.urls import path
from .apis import ProfileApi, RegisterApi, UpdateUser, UpdatePassword, LoginApi, UpdateProfile

urlpatterns = [
    path('register/', RegisterApi.as_view(),name="register"),
    path('profile/', ProfileApi.as_view(),name="profile"),
    path('update_profile/', UpdateProfile.as_view(),name="profile"),
    path('update_user/', UpdateUser.as_view(),name="profile"),
    path('update_password/', UpdatePassword.as_view(),name="profile"),
    path('login/', LoginApi.as_view(),name="profile"),


]
