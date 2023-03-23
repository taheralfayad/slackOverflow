from rest_framework import serializers
from .models import Issue, Solution

class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ["created", "description", "author", "project"]

class SolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = ["created", "issue", "description", "author"]



