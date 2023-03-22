from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from core.models import Issue
from . import serializers

class IssueList(APIView):
    """
    List all issues, or create new one.
    """
    def get(self, request):
        issues = Issue.objects.all()
        serializer = serializers.IssueSerializer(issues, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = serializers.IssueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



