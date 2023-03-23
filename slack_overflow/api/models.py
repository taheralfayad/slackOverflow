from django.db import models

class Issue(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, default="")
    description = models.CharField(max_length=250)
    author = models.CharField(max_length=100)
    project = models.CharField(max_length=100)

    def __str__(self):
        return 'Issue for %s' % self.project

    def __repr__(self):
        return '<Issue: %r>' % self.project

class Solution(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    issue = models.ForeignKey('Issue', on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    author = models.CharField(max_length=100)

    def __str__(self):
        return 'Solution for %s' % self.issue

    def __repr__(self):
        return '<Solution: %r>' % self.issue
