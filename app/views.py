from rest_framework.decorators import api_view
from rest_framework import status, serializers
from rest_framework.response import Response
from .models import User, MusicPost, Song, Comment, Like
from .serializers import UserSerializer,  MusicPostSerializer, \
    SongSerializer, CommentSerializer, LikeSerializer
    

@api_view(['GET'])
def AppOverview(request):
    app_urls = {
        'all_users': '/',
        'Email': '/?email=email',
        'Username': '/?username=username',
        'Date Account Created': '/?date_published=date_published',
        'Add': '/create',
        'Update': '/update/pk',
        'Delete': 'user/pk/delete'
    }

    return Response(app_urls)


@api_view(['POST'])
def add_user(request):
    user = UserSerializer(data=request.data)
    
    # validating for already existing data
    if User.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')

    if user.is_valid():
        user.save()
        return Response(user.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
# BROKEN CODE FROM GEEKS FOR GEEKS 
# @api_view(['GET'])
# def view_users(request):
    
#     # checking for the parameters from the URL
#     if request.query_params:
#         users = User.objects.filter(**request.query_param.dict())
#     else:
#         users = User.objects.all()

#     # if there is something in items else raise error
#     if users:
#         data = UserSerializer(users)
#         return Response(users.data)
#     else:
#         return Response(status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def view_users(request):
    # checking for the parameters from the URL
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)

    # if there is something in items else raise error
    if users:
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)