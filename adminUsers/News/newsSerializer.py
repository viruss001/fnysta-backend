# newsSerializer.py
from rest_framework import serializers
from News.models import Category, Tag, Article

class ArticleSerializer(serializers.ModelSerializer):
    # Input fields
    category = serializers.CharField()
    tags = serializers.ListField(child=serializers.CharField(), required=False)

    # Output fields
    category_name = serializers.SerializerMethodField()
    tags_names = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'slug', 'category', 'tags',
            'category_name', 'tags_names',
            'content', 'image', 'published_at', 'updated_at', 'is_published'
        ]
        read_only_fields = ['id', 'slug', 'published_at', 'updated_at', 'category_name', 'tags_names']

    def get_category_name(self, obj):
        return obj.category.name if obj.category else None

    def get_tags_names(self, obj):
        return [tag.name for tag in obj.tags.all()]

    def create(self, validated_data):
        category_name = validated_data.pop("category")
        tag_names = validated_data.pop("tags", [])

        category, _ = Category.objects.get_or_create(name=category_name)
        article = Article.objects.create(category=category, **validated_data)

        tags = [Tag.objects.get_or_create(name=name)[0] for name in tag_names]
        article.tags.set(tags)
        return article

    def update(self, instance, validated_data):
        category_name = validated_data.pop("category", None)
        tag_names = validated_data.pop("tags", None)

        if category_name:
            category, _ = Category.objects.get_or_create(name=category_name)
            instance.category = category

        if tag_names is not None:
            tags = [Tag.objects.get_or_create(name=name)[0] for name in tag_names]
            instance.tags.set(tags)

        return super().update(instance, validated_data)
