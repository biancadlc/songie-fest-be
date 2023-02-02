from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, serializers
from rest_framework.response import Response
from .models import User, MusicPost, Song, Comment
from .serializers import UserSerializer,  MusicPostSerializer, \
    SongSerializer, CommentSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

# IMPORTANT
# 

# 1) Start using postman

# 2) make sure you are passing the token as an authorization header in postman
#     imagine the token is 123456
#     in post man you would make the authorization value: Token 123456 
#     (space between Token and 123456 and everything without quotes)
# 
# 3) If you are changing an accounts details you need to pass through that 
#     specific users token gain access and change their details

# 4) Do not forget the slash at the end of endpoints
#    if you forget you will get an error message in postman without a response



# ====== Geeks for Geeks tutorial ====== #
# retrieves all the user's data using the objects.all() method.
# Serializes data using UserSerializer.
# Then serialized data is rendered using Response() and returns the result
# many=True arg serializes multiple user instances

# ========================================================== 
#        /register/ ROUTE            
# ==========================================================
# class CustomizedUserPermission(IsAuthenticated):
#     def has_permission(self, request, view):
#         if view.action == 'create':
#             return True
#         return super().has_permission(request, view) 

@api_view(['POST'])
@authentication_classes([]) #disables authentication
@permission_classes([]) #disables permission
def registration_view(request):

    '''
    post request for /register/ endpoint
    you need to use authorization header in postman also dont forget end slash for register/
    '''
    if request.method == 'POST':

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



# ========================================================== 
#        /users/<id>     ROUTE            
# ==========================================================

@api_view(['GET','PUT','PATCH','DELETE'])
@permission_classes([IsAuthenticated])
def account_details(request, pk):

    '''
    If GET, retrieve a single user instance based on primary key (id)
    If PUT, update instance & save to db
    If DELETE, delete the instance from fb
    YOU MUST BE THE USER WHOS INFO YOU ARE ACESSING IN THIS ROUTE
    THIS IS DIFFERENT THAN get_music_posts_one_user
    '''
    try:
        user = User.objects.get(pk=pk)
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
    
    
    
# ==========================================================
#        /home/     ROUTE           
# ========================================================== 
# user has to be logged in (pass token in header) to view music posts
# GET all music posts, create a music post

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def musicpost_list(request):
    '''
    List all music posts, or create a new music post
    '''
    if request.method == 'GET':
        music_post = MusicPost.objects.all()
        serializer = MusicPostSerializer(music_post, many=True)
        return Response(serializer.data)


    elif request.method == 'POST':
        serializer = MusicPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
        
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
#       musicpost/<int:pk>/   ROUTE           
# ========================================================== 


# === GET a SINGLE music post, DELETE a single music post
@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def musicpost_detail(request, pk):
    '''
    If GET, retrieve a single music post based on primary key (music post id)
    If DELETE, delete the instance from db ONLY if you are the owner of the post
    '''
    try:
        music_post = MusicPost.objects.get(pk=pk)
    except MusicPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


    if request.method == 'GET':
        serializer = MusicPostSerializer(music_post)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        user = music_post.user
        requesting_user = request.user
        
        if user != requesting_user:
            return Response({"response": "You don't have permission to access this info becaue you are not the user" })

        operation = music_post.delete()
        data = {}
        if operation:
            data["success"] = "delete successful"
        else: 
            data["failure"] = "delete unsuccessful"
    
        return Response(data=data)
    
    


# =======================================================================================
#     musicpost/<music_post id>/comments/  ROUTE      
# =======================================================================================  

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def comment_list(request, pk):
    '''
    List all comments for a specific music post 
    Create a new comment
    '''
    try:
        music_post = MusicPost.objects.get(pk=pk)
    except MusicPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # retrieve all Comment objects that belong to the MusicPost 
        comments = Comment.objects.filter(music_post=music_post)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, music_post=music_post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# =======================================================================================
#     musicpost/ <musicpost_id> /comments/ <comment_id>  ROUTE      
# =======================================================================================  
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_comment(request, pk, id):
    '''
    delete a specific comment from a music post
    '''
    try:
        music_post = MusicPost.objects.get(pk=pk)
    except MusicPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = music_post.user
    requesting_user = request.user
    if user != requesting_user:
        return Response({"response": "You don't have permission to access this info becaue you are not the user" })

    if request.method == 'DELETE':
        comment = Comment.objects.get(pk=id)
        operation = comment.delete()
        data = {}
        if operation:
            data["success"] = "delete successful"
        else: 
            data["failure"] = "delete unsuccessful"
    
        return Response(data=data)
    

        
