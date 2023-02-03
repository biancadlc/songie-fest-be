from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, serializers
from rest_framework.response import Response
from ..models import User 
from ..serializers import UserSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model


# ========================================================== 
#        /users/     ROUTE            
# ==========================================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_list(request):
    """
    List all users
    
    IMPORTANT: ONLY SONGIEFEST USERS CAN ACCESS THIS
    this is due to needing any users token listed as an authorization header
    """
    if request.method == 'GET':
        # User = get_user_model()
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)


