from django.contrib.auth import login, logout, get_user_model
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from users.serializers import UserSerializer, LoginSerializer
from users.models import LoginDate



class UserRegistrationView(CreateAPIView):
    serializer_class = UserSerializer


class UserLoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.get_user(serializer.validated_data["email"])
        login(request, user)
        
        LoginDate.objects.create(user=user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_user(self, email):
        return get_user_model().objects.filter(email=email).first()


class UserLogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)