from .models import Post
from rest_framework import serializers

#class PostSerializer(serializers.HyperlinkedModelSerializer):
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        #fields = {'url', 'id', 'author', 'title', 'text'}
        fields = '__all__' # all model fields will be included