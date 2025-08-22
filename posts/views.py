# posts/views.py

from rest_framework import viewsets, permissions, authentication
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from .models import Post
from .serializers import PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [authentication.TokenAuthentication]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        
        if user in post.likes.all():
            # User has already liked the post, so unlike it
            post.likes.remove(user)
            return Response({'status': 'unliked'}, status=status.HTTP_200_OK)
        else:
            # User has not liked the post, so like it
            post.likes.add(user)
            return Response({'status': 'liked'}, status=status.HTTP_200_OK)