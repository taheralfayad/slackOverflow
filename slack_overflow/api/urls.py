from django.urls import path
from . import views

urlpatterns = [
    path('issue', views.IssueList.as_view()),
    path('issue/<str:request_project>', views.ProjectList.as_view()),
    path('solution', views.SolutionList.as_view()), 
    path('solution/<int:issue_id>', views.SolutionbyIssue.as_view()),
]
