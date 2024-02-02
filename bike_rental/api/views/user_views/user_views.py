from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from authentication.views.utils import send_activation_mail
from api.serializers import UserSerializer, UserRegistrationSerializer
from api.views.permission import IsSuperUser

User = get_user_model()


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSuperUser]
    serializer_class = UserSerializer


class UserRegister(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data.pop('password2')
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
            user = serializer.save()
            send_activation_mail(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key
        })
