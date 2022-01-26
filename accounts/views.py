from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import SignupSerializer
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated
import jwt
from django.conf import settings
from .models import MyUser
# Create your views here.


class SignupView(APIView):
    serializer_class = SignupSerializer

    def post(self, request):
        print(request.data)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Signup done")
        else:
            return Response(serializer.errors)


class SigninView(APIView):

    def post(self, request):
        def get_tokens_for_user(user):
            refresh = RefreshToken.for_user(user)

            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }

        user = authenticate(request, username=request.data['email'], password=request.data['password'])
        if user is not None:
            login(request, user)
            tokens = get_tokens_for_user(user);
            refreshToken = tokens['refresh']
            accessToken = tokens['access']
            return Response({"message": "Login done", "refreshToken": refreshToken, "accessToken": accessToken})
        else:
            return Response({"error": "Invalid credentials"})



class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        token = request.headers['Authorization'].split(' ')[1]
        print(token)
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

        user_id = payload['user_id']

        try:
            user = MyUser.objects.get(pk=user_id)
            return Response({"message": "Protected view"})
        except MyUser.DoesNotExist:
            return Response({"message": "No user found"})
