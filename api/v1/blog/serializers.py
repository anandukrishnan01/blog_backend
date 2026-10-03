from rest_framework import serializers
from blog.models import Blog
from django.contrib.auth.models import User

class BlogSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Blog
        fields = ['id', 'author', 'author_username', 'title', 'image', 'content', 'created_at', 'updated_at']
        read_only_fields = ['author']
