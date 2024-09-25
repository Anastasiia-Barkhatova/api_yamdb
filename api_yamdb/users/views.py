from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.constants import MAX_PAGE_SIZE, PAGE_SIZE, PAGE_SIZE_QUERY_PARAM
from users.permissions import IsAdminUser, IsSelf
from users.serializers import SignUpSerializer, TokenSerializer, UserSerializer

User = get_user_model()


class SignUpView(APIView):
    """Представление для регистрации пользователя."""

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """Создание нового пользователя."""
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            username = serializer.validated_data.get('username')
            if (User.objects.filter(email=email).exists()
                    and not User.objects.filter(username=username).exists()):
                return Response(
                    {'error':
                     'Пользователь с таким email уже зарегистрирован'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user = serializer.save()
            user_data = {
                'email': user.email,
                'username': user.username
            }
            return Response(user_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenView(APIView):
    """Представление для генерации токена для пользователей."""

    permission_classes = [AllowAny]

    def post(self, request):
        """Создание токена для пользователя."""
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            confirmation_code = serializer.validated_data['confirmation_code']

            user = get_object_or_404(User, username=username)

            if user and user.check_password(confirmation_code):
                refresh = RefreshToken.for_user(user)
                return Response({'token': str(refresh.access_token)},
                                status=status.HTTP_200_OK)
            return Response({'detail':
                            'Invalid username or confirmation code.'},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserPagination(PageNumberPagination):
    """Класс пагинации для UserViewSet."""

    page_size = PAGE_SIZE
    page_size_query_param = PAGE_SIZE_QUERY_PARAM
    max_page_size = MAX_PAGE_SIZE


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet для управления пользователями."""

    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer
    pagination_class = UserPagination
    lookup_field = 'username'
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_permissions(self):
        """Получение разрешений для действий."""
        if self.action in ['list', 'create']:
            self.permission_classes = [IsAdminUser]
        elif self.action == 'destroy':
            if self.kwargs.get('username') == 'me':
                self.permission_classes = [IsAuthenticated]
            else:
                self.permission_classes = [IsAdminUser]
        elif self.action in ['retrieve', 'update', 'partial_update']:
            if self.kwargs.get('username') == 'me':
                self.permission_classes = [IsAuthenticated]
            else:
                self.permission_classes = [IsAdminUser, IsSelf]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def get_object(self):
        """Получение объекта пользователя."""
        username = self.kwargs.get('username')
        if username == 'me':
            return self.request.user
        return get_object_or_404(User, username=username)

    def destroy(self, request, *args, **kwargs):
        """Удаление пользователя, если это не /me."""
        if self.kwargs.get('username') == 'me':
            return Response(
                {'error': 'DELETE запрос на /me не разрешен'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return super().destroy(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """Частичное обновление пользователя."""
        if 'role' in request.data and self.kwargs.get('username') == 'me':
            return Response(
                {'error': 'Вы не можете менять роль пользователя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        elif (not request.user.is_admin
              and request.user.is_authenticated
              and self.kwargs.get('username') != 'me'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().partial_update(request, *args, **kwargs)
