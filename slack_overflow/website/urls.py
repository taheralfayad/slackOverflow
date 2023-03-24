from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('project/<project>/', views.project, name='project'),
    path('issue/<issue>', views.issueContainer, name='issue')
]
