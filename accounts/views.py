from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.timezone import now
from .models import AccessKey
from .serializers import LoginSerializer, AccessKeySerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        try:
            access_key = AccessKey.objects.get(username=username)
            if not access_key.check_password(password):
                return Response({'error': 'Invalid credentials'}, status=403)

            if not access_key.is_active:
                return Response({'error': 'Access key is inactive'}, status=403)

            if access_key.is_quota_exceeded:
                access_key.invalidate_key(reason='Quota exceeded')
                return Response({'error': 'Quota exceeded'}, status=403)

            if access_key.has_credential_expired:
                access_key.invalidate_key(reason='Credential expired')
                return Response({'error': 'Credential expired'}, status=403)

            if not access_key.first_login_time:
                access_key.first_login_time = now()

            access_key.current_session_start_time = now()
            access_key.save()

            refresh = RefreshToken.for_user(access_key)
            return Response({'access': str(refresh.access_token), 'refresh': str(refresh)}, status=200)

        except AccessKey.DoesNotExist:
            return Response({'error': 'Access key not found'}, status=404)

class SessionStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        access_key = request.user
        if access_key.current_session_start_time:
            elapsed_time = (now() - access_key.current_session_start_time).total_seconds() / 60
            access_key.total_minutes_used += int(elapsed_time)
            access_key.current_session_start_time = now()
            access_key.last_active_time = now()
            access_key.save()

        if access_key.is_quota_exceeded or access_key.has_credential_expired:
            access_key.invalidate_key()
            return Response({'error': 'Session invalidated'}, status=403)

        return Response({'status': 'active', 'minutes_used': access_key.total_minutes_used}, status=200)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        access_key = request.user
        if access_key.current_session_start_time:
            elapsed_time = (now() - access_key.current_session_start_time).total_seconds() / 60
            access_key.total_minutes_used += int(elapsed_time)
            access_key.current_session_start_time = None
            access_key.save()

        refresh = RefreshToken(request.auth)
        refresh.blacklist()

        return Response({'status': 'logged out'}, status=200)

@csrf_exempt
def run_maintenance(request):
    if request.method == 'GET':
        # Invalidate expired or quota-exceeded keys
        keys = AccessKey.objects.filter(is_active=True)
        for key in keys:
            if key.is_quota_exceeded or key.has_credential_expired:
                key.invalidate_key()

        # Delete keys scheduled for deletion
        keys_to_delete = AccessKey.objects.filter(is_active=False, scheduled_for_deletion__lte=now())
        keys_to_delete.delete()

        return JsonResponse({'status': 'Maintenance tasks executed successfully'})
    return JsonResponse({'error': 'Invalid request method'}, status=400)
