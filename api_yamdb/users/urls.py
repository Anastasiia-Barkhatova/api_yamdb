from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import SignUpView, TokenView, UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('v1/auth/signup/', SignUpView.as_view(), name='signup'),
    path('v1/auth/token/', TokenView.as_view(), name='token'),
    path('v1/', include(router.urls)),
]
