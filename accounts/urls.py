from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoginView, SessionStatusView, LogoutView, run_maintenance, AccessKeyViewSet

router = DefaultRouter()
router.register(r'access-keys', AccessKeyViewSet, basename='accesskey')

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('session/status/', SessionStatusView.as_view(), name='session_status'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('run_maintenance/', run_maintenance, name='run_maintenance'),
    path('', include(router.urls)),
]
