from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from .models import Issue, Solution
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
    


class SolutionList(APIView): 
    """
    List all solutions, get a solution for a given issue, or create new one
    """
    def get(self, request):
        solutions = Solution.objects.all()
        serializer = serializers.SolutionSerializer(solutions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.SolutionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SolutionbyIssue(APIView):
    """
    Get solution for specific issue
    """
    def get(self, request, issue_id):
        try:
            solutions = Solution.objects.filter(issue=issue_id)
        except Solution.DoesNotExist:
            raise Http404("No solutions exist")
        serializer = serializers.SolutionSerializer(solutions, many=True)
        return Response(serializer.data)

class ProjectList(APIView):
    """
    Get all issues for certain project.
    """
    def get(self, request, request_project):
        try:
            issues = Issue.objects.filter(project=request_project)
        except Issue.DoesNoteExist:
            raise Http404("No issues exist for given project.")
        serializer = serializers.IssueSerializer(issues, many=True)
        return Response(serializer.data) 
