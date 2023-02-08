
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
    # try:
    #     user = User.objects.get(username=request.data['username'])
    # except User.DoesNotExist:
    #     return Response(status=status.HTTP_404_NOT_FOUND)
    # if password == user.password:
    #     data = {'response': 'Success'}
    return Response(status=status.HTTP_200_OK)

    # if request.method == 'GET':
    #     id = user.pk
    #     music_posts = MusicPost.objects.filter(user=id)
    #     serializer = MusicPostSerializer(music_posts, many=True)
    #     return Response(serializer.data)

    
    # elif request.method == 'POST':
    #     requesting_user = request.user
    #     if user != requesting_user:
    #         return Response({"response": "You don't have permission to access this info because you are not the user" })

    #     request.data['user'] = user.pk
    #     request.data['username'] = user.username
    #     serializer = MusicPostSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()        
    #         return Response(serializer.data,
    #                             status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors,
    #                         status=status.HTTP_400_BAD_REQUEST)
