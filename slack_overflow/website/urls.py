from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('project/<project>/', views.issueContainer, name='issue')
]
