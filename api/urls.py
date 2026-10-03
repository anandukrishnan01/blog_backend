from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status

class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=username, password=password)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'username': user.username}, status=status.HTTP_201_CREATED)

class CustomAuthToken(APIView):
    def post(self, request):
        from rest_framework.authtoken.views import ObtainAuthToken
        response = ObtainAuthToken.as_view()(request=request._request)
        if response.status_code == 200:
            token = Token.objects.get(key=response.data['token'])
            return Response({'token': token.key, 'username': token.user.username})
        return response

urlpatterns = [
    path('v1/blog/', include('api.v1.blog.urls')),
    path('auth/login/', CustomAuthToken.as_view(), name='api_token_auth'),
    path('auth/register/', RegisterView.as_view(), name='api_register'),
]
