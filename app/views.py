from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, serializers
from rest_framework.response import Response
from .models import User, MusicPost, Song, Comment, Like
from .serializers import UserSerializer,  MusicPostSerializer, \
    SongSerializer, CommentSerializer, LikeSerializer
        

# @api_view(['GET'])
# def AppOverview(request):
#     app_urls = {
#         'all_users': '/',
#         'Email': '/?email=email',
#         'Username': '/?username=username',
#         'Date Account Created': '/?date_published=date_published',
#         'Add': '/create',
#         'Update': '/update/pk',
#         'Delete': 'user/pk/delete'
#     }

#     return Response(app_urls)


# @api_view(['POST'])
# def add_user(request):
#     user = UserSerializer(data=request.data)
    
#     # validating for already existing data
#     if User.objects.filter(**request.data).exists():
#         raise serializers.ValidationError('This data already exists')

#     if user.is_valid():
#         user.save()
#         return Response(user.data)
#     else:
#         return Response(status=status.HTTP_404_NOT_FOUND)
    
# # BROKEN CODE FROM GEEKS FOR GEEKS 
# # @api_view(['GET'])
# # def view_users(request):
    
# #     # checking for the parameters from the URL
# #     if request.query_params:
# #         users = User.objects.filter(**request.query_param.dict())
# #     else:
# #         users = User.objects.all()

# #     # if there is something in items else raise error
# #     if users:
# #         data = UserSerializer(users)
# #         return Response(users.data)
# #     else:
# #         return Response(status=status.HTTP_404_NOT_FOUND)
    
# @api_view(['GET'])
# def view_users(request):
#     # checking for the parameters from the URL
#     users = User.objects.all()
#     serializer = UserSerializer(users, many=True)

#     # if there is something in items else raise error
#     if users:
#         return Response(serializer.data)
#     else:
#         return Response(status=status.HTTP_404_NOT_FOUND)
    

# @api_view(['POST'])
# def update_users(request, pk):
#     user = User.objects.get(pk=pk)
#     data = UserSerializer(instance=user, data=request.data)

#     if data.is_valid():
#         data.save()
#         return Response(data.data)
#     else:
#         return Response(status=status.HTTP_404_NOT_FOUND)



    

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
        


# === GET ALL music postS for a user, CREATE ONE music post for a user

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def musicpost_list(request, user_id):
    '''
    List all music posts, or create a new music post for a user 
    '''
    
    
    
        
# === GET a SINGLE music post, DELETE a single music post
# === UPDATE like/comment on a single music post 
@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def musicpost_detail(request, pk):
    '''
    If GET, retrieve a single music post based on primary key (music post id)
    If DELETE, delete the instance from db
    If PATCH, like or comment on a music post
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
    

    
    # elif request.method == 'PATCH':
    #     serializer = MusicPostSerializer(music_post,
    #                                 data=request.data,
    #                                 partial=True)

    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors,
    #                     status=status.HTTP_400_BAD_REQUEST)
        

# need routes for like & comment 
    # "/<musicpost_id>/like"
    # "/<musicpost_id>/comment"
    
@api_view(['PATCH'])
def musicpost_like(request, pk):
    '''
    Like a music post 
    '''
    try:
        music_post = MusicPost.objects.get(pk=pk)
    except MusicPost.DoesNotExist:
        return Response(status=status.HTPP_404_NOT_FOUND)
    
    
    if request.method == 'PATCH':
        serializer = MusicPostSerializer(music_post,
                                        data=request.data,
                                        partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
        
    # music_post.save()
    # return Response({"message": "Music post liked!"})


@api_view(['PATCH'])
def musicpost_comment(request, pk):
    '''
    Comment on a music post
    '''
    try:
        music_post = MusicPost.objects.get(pk=pk)
    except MusicPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PATCH':
        serializer = MusicPostSerializer(music_post,
                                        data=request.data,
                                        partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
        
