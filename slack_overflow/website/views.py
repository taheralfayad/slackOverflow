from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.forms.models import model_to_dict
from api.models import Issue, Solution

# Create your views here.
def index(request):
    if request.method == 'POST':
        project = request.POST['project']
        url = reverse('project', kwargs={'project': project})
        return HttpResponseRedirect(url)
    return render(request, "index.html")

def project(request, project):
    if request.method == 'POST':
        id = request.POST['issue']
        url = reverse('issue', kwargs={'issue': id})
        return HttpResponseRedirect(url)
    issues = Issue.objects.filter(project=project).values()
    issues_list = list(issues)
    context = {
        "project": project,
        "issues": issues_list
    }
    return render(request, "project.html", context)

def issueContainer(request, issue):
    if request.method == 'POST':
        answer = request.POST['answer']
        attached_issue = Issue.objects.get(id=issue)
        new_answer = Solution(description=answer, issue = attached_issue)
        new_answer.save()
    issue_query = Issue.objects.filter(id=issue).values()
    solution = Solution.objects.filter(issue__pk=issue).values()
    solution_list = list(solution)
    issue_list = list(issue_query)
    context = {
        "issue": issue_list[0],
        "solutions": solution_list
    }
    return render(request, "issue.html", context)
