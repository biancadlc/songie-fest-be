from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, serializers
from rest_framework.response import Response
from .models import User, MusicPost, Song, Comment
from .serializers import UserSerializer,  MusicPostSerializer, \
    SongSerializer, CommentSerializer


# ====== Geeks for Geeks tutorial ====== #
# retrieves all the user's data using the objects.all() method.
# Serializes data using UserSerializer.
# Then serialized data is rendered using Response() and returns the result
# many=True arg serializes multiple user instances

# ============================= 
#        USER ROUTES            
# ============================= 
@api_view(['GET','POST'])
def user_list(request):
    """
    List all users, or create a new user
    """
    if request.method == 'GET':
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # create_message = f"User has been successfully created"
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET','PUT','PATCH','DELETE'])
def user_detail(request, pk):
    '''
    If GET, retrieve a single user instance based on primary key (id)
    If PUT, update instance & save to db
    If DELETE, delete the instance from fb
    '''
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

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
        # delete_message = f'User {pk} has been deleted'
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    
# ============================= 
#        MUSIC POST ROUTES            
# ============================= 
# user has to be logged in to view/delete music post 
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
        

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def get_music_posts_one_user(request, username):
    '''
    List all music posts for a user 
    Create a new music post for a user
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
        serializer = MusicPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


# === GET a SINGLE music post, DELETE a single music post
@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def musicpost_detail(request, pk):
    '''
    If GET, retrieve a single music post based on primary key (music post id)
    If DELETE, delete the instance from db
    '''
    try:
        music_post = MusicPost.objects.get(pk=pk)
    except MusicPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MusicPostSerializer(music_post)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        music_post.delete()
        # delete_message = f'Music Post {pk} has been deleted'
        return Response(status=status.HTTP_204_NO_CONTENT)
    


# ============================= 
#      COMMENT/LIKE  ROUTES            
# =============================      
# UPDATE like/comment on a single music post === #
# need routes for like & comment 
    # "/<musicpost_id>/like"
    # "/<musicpost_id>/comment"

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
    

# ===== LIKE a Music Post ===== #
api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def like_music_post(request, pk):
    '''
    Like a music post
    '''
    try:
        music_post = MusicPost.objects.get(pk=pk)
    except MusicPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PATCH':
        music_post.likes_count += 1
        music_post.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    
    

        
