from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, serializers
from rest_framework.response import Response
from ..models import User, MusicPost, Song, Comment
from ..serializers import UserSerializer
from rest_framework.authtoken.models import Token






@api_view(['POST'])
@authentication_classes([]) #disables authentication
@permission_classes([]) #disables permission
def register_view(request):

    '''
    post request for /register/ endpoint
    you need to use authorization header in postman also dont forget end slash for register/
    '''
    # try:
        # put for loop here lines 55 -58
    serializer = UserSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        user = serializer.save()
        data['email'] = user.email
        data['username'] = user.username
        token = Token.objects.get(user=user).key
        data['token'] = token
    else:
        data = serializer.errors
    return Response(data)
    # except:
    #     message = {'detail': 'User with this email already exists'}
    #     return Response(message, status=status.HTTP_400_BAD_REQUEST)