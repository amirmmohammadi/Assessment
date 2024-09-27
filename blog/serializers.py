from rest_framework import serializers

from .models import Content, ContentScore


class ContentSerializer(serializers.ModelSerializer):
    user_score = serializers.SerializerMethodField()

    class Meta:
        model = Content
        exclude = ('deleted_at', 'is_deleted', 'calculated_to',)

    def get_user_score(self, obj):
        return obj.user_score if hasattr(obj, 'user_score') else None


class ContentScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentScore
        exclude = ('is_spam', 'owner')
