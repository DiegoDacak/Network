from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    date = serializers.DateTimeField(format="%B %d, %Y, %I:%S %p")
    class Meta:
        model = Post
        # fields = ('id', 'user', 'date', 'post', 'like')
        fields = '__all__'