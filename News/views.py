from rest_framework import generics
from .models import Category, Tag, Article
from .serializers import CategorySerializer, TagSerializer, ArticleSerializer


# -------- Categories --------
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# -------- Tags --------
class TagListView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TagDetailView(generics.RetrieveAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


# -------- Articles --------
class ArticleListView(generics.ListAPIView):
    """
    GET /articles/ -> list all articles
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class ArticleDetailView(generics.RetrieveAPIView):
    """
    GET /articles/<id>/ -> get single article by id
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
