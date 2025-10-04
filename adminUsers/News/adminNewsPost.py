# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from News.models import Article
from .newsSerializer import ArticleSerializer
from ..utils import checkUserIsAuthenticated
from django.views.decorators.csrf import csrf_exempt

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # disable CSRF

@api_view(['POST'])
@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def create_article(request):
    if checkUserIsAuthenticated(request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"detail": "User is not logged in"}, status=status.HTTP_401_UNAUTHORIZED)

# UPDATE
@csrf_exempt
@api_view(['PUT', 'PATCH'])
def update_article(request, pk):
    if checkUserIsAuthenticated(request):
        try:
            article = Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return Response({"detail": "Article not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ArticleSerializer(article, data=request.data, partial=(request.method=='PATCH'))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"detail": "User is not logged in"}, status=status.HTTP_401_UNAUTHORIZED)

# DELETE
@csrf_exempt
@api_view(['DELETE'])
def delete_article(request, pk):
    if checkUserIsAuthenticated(request):
        try:
            article = Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return Response({"detail": "Article not found"}, status=status.HTTP_404_NOT_FOUND)

        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response({"detail": "User is not logged in"}, status=status.HTTP_401_UNAUTHORIZED)
