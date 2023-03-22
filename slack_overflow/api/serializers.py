from rest_framework import serializers
from core.models import Issue

class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ["created", "text", "author", "project_id"]

