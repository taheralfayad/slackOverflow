from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.http import Http404

from api.models import Issue, Solution, Project
from api import serializers

# LIST ALL
class ProjectList(APIView):
    '''
    List all projects or create one
    '''
    def get(self, request):
        projects = Project.objects.all()
        serializer = serializers.ProjectSerializer(projects, many=True)
        return Response(serializer.data)
    def post(self, request):
        try:
            project = Project.objects.get(name=request.data['name']) 
            raise Http404(f"Project {request.data['name']} already exists.")   
        except Project.DoesNotExist:
            serializer = serializers.ProjectSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class IssueList(APIView):
    """
    List all issues
    """
    def get(self, request):
        issues = Issue.objects.all()
        serializer = serializers.IssueSerializer(issues, many=True)
        return Response(serializer.data)

class SolutionList(APIView): 
    """
    List all solutions
    """
    def get(self, request):
        solutions = Solution.objects.all()
        serializer = serializers.SolutionSerializer(solutions, many=True)
        return Response(serializer.data)

class ProjectQuery(APIView):
    '''
    GET one project by its name
    '''
    def get(self, request, project_name):
        try:
            project = Project.objects.filter(name=project_name)
        except Project.DoesNotExist:
            raise Http404(f"Project {project_name} does not exist.")
        
        serializer = serializers.ProjectSerializer(project)
        return Response(serializer.data)

class IssueQuery(APIView):
    '''
    GET one issue by its id
    '''
    def get(self, request, issue_id):
        try:
            issue = Issue.objects.get(id=issue_id)
        except Issue.DoesNotExist:
            raise Http404(f"Issue {issue_id} does not exist.")
        
        serializer = serializers.IssueSerializer(issue)
        return Response(serializer.data)
    
class SolutionQuery(APIView):
    '''
    GET one solution by its id
    '''
    def get(self, request, solution_id):
        try:
            solution = Solution.objects.filter(id=solution_id)
        except Solution.DoesNotExist:
            raise Http404(f"Solution {solution_id} does not exist.")
        
        serializer = serializers.IssueSerializer(solution)
        return Response(serializer.data)

class IssueByProject(APIView):
    '''
    List all issues of a project or create an issue for a project
    '''
    def get(self, request, project_name):
        try:
            project = Project.objects.filter(name=project_name)
            issues_of_project = Issue.objects.filter(project=project)
        except Project.DoesNotExist:
            raise Http404(f"Project {project_name} does not exist.")
        
        serializer = serializers.IssueSerializer(issues_of_project, many=True)
        return Response(serializer.data)

    def post(self, request, project_name):
        try:
            project = Project.objects.get(name=project_name) 
        except Project.DoesNotExist:
            raise Http404(f"Project {project_name} does not exist.")
        
        serializer = serializers.IssueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            project.numIssues = project.numIssues + 1
            project.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SolutionbyIssue(APIView):
    """
    Get solution for specific issue
    """
    def get(self, request, issue_id):
        try:
            issue = Issue.objects.filter(id=issue_id)
            solutions_of_issue = Solution.objects.filter(issue=issue)
        except Issue.DoesNotExist:
            raise Http404(f"Issue {issue_id} does not exist.")
        serializer = serializers.SolutionSerializer(solutions_of_issue, many=True)
        return Response(serializer.data)

    def post(self, request, issue_id):
        try:
            issue = Issue.objects.get(id=issue_id) 
        except Issue.DoesNotExist:
            raise Http404(f"Issue {issue_id} does not exist.")
        serializer = serializers.SolutionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
