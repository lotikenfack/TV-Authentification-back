from django.urls import path
from .views import LoginView, SessionStatusView, LogoutView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('session/status/', SessionStatusView.as_view(), name='session_status'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
