from django.urls import include, path
from rest_framework.routers import DefaultRouter

# from rest_framework_simplejwt.views import TokenObtainPairView
from .views import UserViewSet, signup, token

router_v1 = DefaultRouter()

router_v1.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', signup.as_view()),
    path('v1/auth/token/', token.as_view()),
]
