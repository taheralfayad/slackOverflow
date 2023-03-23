from rest_framework import serializers
from .models import Issue, Solution

class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ["id", "created", "title", "description", "author", "project"]

class SolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = ["id", "created", "issue", "description", "author"]



