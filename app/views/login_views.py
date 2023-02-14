
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, serializers
from rest_framework.response import Response
from .. models import  User
from ..serializers import  MusicPostSerializer

from django.contrib.auth import get_user_model

# ==========================================================
#        /login/     ROUTE           
# ========================================================== 


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def login_user(request):
    '''
    logs in user
    '''
    try:
        user = User.objects.get(username=request.data['username'])
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if user.password == request.data['password']:
        
        return Response(status=status.HTTP_200_OK)
    else:
        data = {'response': 'Incorrect Password'}
        return Response(data, status=status.HTTP_401_UNAUTHORIZED)

