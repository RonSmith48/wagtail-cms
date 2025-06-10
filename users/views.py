from django.shortcuts import render
from django.contrib.auth import login
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from users.authentication import JWTAuthenticationFetchUser

@api_view(['POST'])
@permission_classes([AllowAny])
def bridge_login_view(request):
    jwt_auth = JWTAuthenticationFetchUser()

    try:
        validated = jwt_auth.authenticate(request)
        print("Validated:", validated)
    except Exception as e:
        return Response({'detail': f'JWT exception: {str(e)}'}, status=401)

    if not validated:
        return Response({'detail': 'Invalid or missing JWT'}, status=401)

    user, token = validated
    user.backend = 'users.authentication.JWTAuthenticationFetchUser'
    login(request, user)
    return Response({'detail': 'Session created and user synced'})

