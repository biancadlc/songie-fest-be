from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, MusicPost, Song, Comment, Like
from .serializers import UserSerializer,  MusicPostSerializer, \
    SongSerializer, CommentSerializer, LikeSerializer
    

@api_view(['GET'])
def AppOverview(request):
    app_urls = {
        'all_items': '/',
        'Search by Category': '/?category=category_name',
        'Search by Subcategory': '/?subcategory=category_name',
        'Add': '/create',
        'Update': '/update/pk',
        'Delete': 'item/pk/delete'
    }

    return Response(app_urls)

