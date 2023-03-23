from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from api.models import Issue, Solution

# Create your views here.
def index(request):
    if request.method == 'POST':
        project = request.POST['project']
        print(project)
        url = reverse('issue', kwargs={'project': project})
        return HttpResponseRedirect(url)
    return render(request, "index.html")

def issueContainer(request, project):
    issues = Issue.objects.filter(project=project).values()
    context = {
        "project": project,
        "issues": issues
    }
    return render(request, "issue.html", context)
