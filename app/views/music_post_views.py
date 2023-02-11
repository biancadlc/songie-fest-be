from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, serializers
from rest_framework.response import Response
from ..models import User, MusicPost, Song, Comment
from ..serializers import UserSerializer,  MusicPostSerializer, \
    SongSerializer, CommentSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model



# ==========================================================
#       musicpost/<int:pk>/   ROUTE           
# ========================================================== 


# === GET a SINGLE music post, DELETE a single music post
@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def music_post_details(request, pk):
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
        print(serializer.data)
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
    
# =======================================================================================
#     musicpost/ get-username /<commentid> ROUTE      THIS IS NEWW
# =======================================================================================  
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_username(request, commentid):
    '''
    returns username that posted comment when supplied comment id
    '''
    try:
        comment = Comment.objects.get(pk=commentid)
    except MusicPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    data = {}
    data['username'] = comment.user.username
    return Response(data)