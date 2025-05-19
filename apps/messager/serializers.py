from rest_framework import serializers

from .models import (
    Message,
    MessageVisualization,
)

from apps.accounts.serializers import (
    ProfileAuthorSerializer,
)

class MessageVisualizationSerializer(serializers.ModelSerializer):
    viewer_set = ProfileAuthorSerializer(source='viewer',
                                   read_only=True)
    class Meta:
        model = MessageVisualization
        fields = [
            'id',
            'viewer',
            'viewer_set',
            'message',
            'date',
        ]

class MessageSerializer(serializers.ModelSerializer):
    author_set = ProfileAuthorSerializer(source='author',
                                   read_only=True)

    mentions_set = ProfileAuthorSerializer(source='mentions',
                                     many=True,
                                     read_only=True)

    views_by_profile = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            'id',
            'created_at',
            'author',
            'author_set',
            'module',
            'thread',
            'message',
            'mentions',
            'mentions_set',
            'views_by_profile',
        ]

    def get_views_by_profile(self, obj):
        grouped_data = []

        for view in obj.viewers.all():
            profile = view.viewer
            serialized_profile = ProfileAuthorSerializer(profile).data

            if serialized_profile not in grouped_data:
                grouped_data.append(serialized_profile)

        return grouped_data
