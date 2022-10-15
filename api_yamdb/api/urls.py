from django.urls import path

# from rest_framework_simplejwt.views import TokenObtainPairView
from .views import get_token, signup

urlpatterns = [
    path(
        'v1/auth/signup/', signup, name='signup'
    ),
    path(
        'v1/auth/token/', get_token, name='get_token'
    )
]
