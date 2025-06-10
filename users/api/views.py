# users/api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.api.serializers import RemoteUserSerializer

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # request.user is the RemoteUser fetched/created by your auth class
        return Response(RemoteUserSerializer(request.user).data)
