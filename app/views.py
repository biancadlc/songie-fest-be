from rest_framework.decorators import api_view
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
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT','PATCH','DELETE'])
def user_detail(request, pk):
    '''
    If GET, retrieve a single user instance based on primary key
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
        return Response(status=status.HTTP_204_NO_CONTENT)