from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import IsAdminUser, IsModeratorUser, IsAuthorOrReadOnly
from .serializers import SignUpSerializer, UserSerializer, TokenSerializer
from rest_framework.pagination import PageNumberPagination

User = get_user_model()

class SignUpView(APIView):
    permission_classes = []  # Отключаем требование аутентификации для регистрации

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TokenView(APIView):
    permission_classes = []  # Отключаем требование аутентификации для получения токена

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            confirmation_code = serializer.validated_data['confirmation_code']
            user = User.objects.filter(username=username).first()
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
        if not username:
            raise User.DoesNotExist("User matching query does not exist.")
        return User.objects.get(username=username)
