from django.urls import path
from api import views

urlpatterns = [
    # Query All
    path('projects', views.ProjectList.as_view()),
    path('issues', views.IssueList.as_view()),
    path('solutions', views.SolutionList.as_view()),

    # Query GET 1
    path('projects/<str:project_name>', views.ProjectQuery.as_view()),
    path('issues/<int:issue_id>', views.IssueQuery.as_view()),
    path('solutions/<int:solution_id>', views.SolutionQuery.as_view()),

    # Retrieve all issues of a project, all solutions of a project, or POST
    path('projects/<str:project_name>/issues', views.IssueByProject.as_view()),
    path('issues/<int:issue_id>/solutions', views.SolutionbyIssue.as_view()),
]
