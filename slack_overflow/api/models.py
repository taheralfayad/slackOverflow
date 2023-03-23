from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    numIssues = models.PositiveIntegerField(default=0)

    def __str__(self):
        return 'Project %s' % self.name
    
    def __repr__(self):
        return '<Project: %r>' % self.name


class Issue(models.Model):
    title = models.CharField(max_length=100, default="")
    created = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=500)
    author = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return 'Issue for %s' % self.project

    def __repr__(self):
        return '<Issue: %r>' % self.project

class Solution(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    author = models.CharField(max_length=100)

    def __str__(self):
        return 'Solution for %s' % self.issue

    def __repr__(self):
        return '<Solution: %r>' % self.issue
