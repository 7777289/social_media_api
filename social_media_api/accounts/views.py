# accounts/views.py
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication


from .models import User
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
serializer_class = RegisterSerializer
permission_classes = [permissions.AllowAny]


def create(self, request, *args, **kwargs):
serializer = self.get_serializer(data=request.data)
serializer.is_valid(raise_exception=True)
user = serializer.save()
token, _ = Token.objects.get_or_create(user=user)
data = {
'token': token.key,
'user': UserSerializer(user, context={'request': request}).data,
}
return Response(data, status=status.HTTP_201_CREATED)


class LoginView(ObtainAuthToken):
serializer_class = LoginSerializer


def post(self, request, *args, **kwargs):
serializer = self.serializer_class(data=request.data, context={'request': request})
serializer.is_valid(raise_exception=True)
user = serializer.validated_data['user']
token, _ = Token.objects.get_or_create(user=user)
return Response({
'token': token.key,
'user': UserSerializer(user, context={'request': request}).data,
})


class ProfileView(generics.RetrieveUpdateAPIView):
serializer_class = UserSerializer
authentication_classes = [TokenAuthentication]
permission_classes = [permissions.IsAuthenticated]


def get_object(self):
return self.request.user