
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, serializers
from rest_framework.response import Response
from .. models import  MusicPost
from ..serializers import  MusicPostSerializer

from django.contrib.auth import get_user_model

# ==========================================================
#        /explore/     ROUTE           
# ========================================================== 
# user has to be logged in (pass token in header) to view music posts
# GET all music posts, create a music post

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def explore_posts(request):
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