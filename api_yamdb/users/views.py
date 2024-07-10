from rest_framework import viewsets, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated

from users.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from .permissions import IsAdminUser, IsModeratorUser, IsAuthorOrReadOnly
from .serializers import SignUpSerializer, UserSerializer, TokenSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError


User = get_user_model()


class SignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user_data = {
                'email': user.email,
                'username': user.username
            }
            return Response(user_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class TokenView(APIView):
    permission_classes = [AllowAny]  # Отключаем требование аутентификации для получения токена

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            confirmation_code = serializer.validated_data['confirmation_code']

            # Изменение: использование get_object_or_404 для проверки существования пользователя
            user = get_object_or_404(User, username=username)

            if user and user.check_password(confirmation_code):
                refresh = RefreshToken.for_user(user)
                return Response({'token': str(refresh.access_token)}, status=status.HTTP_200_OK)
            return Response({'detail': 'Invalid username or confirmation code.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = UserPagination
    lookup_field = 'username'
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']  # Добавьте поля, по которым будет производиться поиск
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_permissions(self):
        if self.action in ['list', 'create', 'destroy']:
            self.permission_classes = [IsAdminUser]
        elif self.action in ['retrieve', 'update', 'partial_update']:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def get_object(self):
        username = self.kwargs.get('username')
        if username == 'me':
            return self.request.user
        return get_object_or_404(User, username=username)
