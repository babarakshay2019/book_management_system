from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from users.serializers import CustomUserSerializer, LogoutSerializer
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['email', 'user_type']  # Filter by email and user_type
    search_fields = ['first_name', 'last_name', 'email']  # Search fields
    ordering_fields = ['created_at', 'email']  # Allow ordering

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def logout(self, request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            # Call the save method to blacklist the refresh token
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
