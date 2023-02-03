

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, serializers
from rest_framework.response import Response
from ..models import User, MusicPost
from ..serializers import UserSerializer,  MusicPostSerializer, \
    SongSerializer, CommentSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model



        
# ==========================================================
#        /<username>/     ROUTES           
# ========================================================== 
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def profile_view(request, username):
    '''
    List all music posts for a user 
    GET requests can be done with anyones token
    (you dont have to be THE user who youre stalking)

    To post to this endpoint THO you must be THE user with the same username as the endpoint
    '''
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        id = user.pk
        music_posts = MusicPost.objects.filter(user=id)
        serializer = MusicPostSerializer(music_posts, many=True)
        return Response(serializer.data)

    
    elif request.method == 'POST':
        requesting_user = request.user
        if user != requesting_user:
            return Response({"response": "You don't have permission to access this info because you are not the user" })

        request.data['user'] = user.pk
        request.data['username'] = user.username
        serializer = MusicPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()        
            return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


# ========================================================== 
#          /<username>/account    ROUTES                 
# ==========================================================

@api_view(['GET','PUT','PATCH','DELETE'])
@permission_classes([IsAuthenticated])
def account_details(request, username):

    '''
    If GET, retrieve a single user instance based on primary key (id)
    If PUT, update instance & save to db
    If DELETE, delete the instance from fb
    YOU MUST BE THE USER WHOS INFO YOU ARE ACESSING IN THIS ROUTE
    THIS IS DIFFERENT THAN get_music_posts_one_user
    '''
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    
    requesting_user = request.user # checks token passed through request
    if user != requesting_user:
        return Response({"response": "You don't have permission to access this info becaue you are not the user" })


    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'PATCH':
        serializer = UserSerializer(user,
                                    data=request.data,
                                    partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
    
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    
