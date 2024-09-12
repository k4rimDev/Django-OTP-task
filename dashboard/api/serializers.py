from rest_framework import serializers

from dashboard.models import File, Comment


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'owner', 'file', 'description', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'file', 'user', 'text', 'created_at']
