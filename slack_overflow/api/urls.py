from django.urls import path
from . import views

urlpatterns = [
    path('issue', views.IssueList.as_view()),
]
