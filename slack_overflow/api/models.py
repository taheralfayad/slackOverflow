from django.db import models

class Issue(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=250)
    author = models.CharField(max_length=100)
    project_id = models.ForeignKey('Project', models.CASCADE)

    def __str__(self):
        return 'Issue for %s' % self.project

    def __repr__(self):
        return '<Issue: %r>' % self.project

class Project(models.Model):
    title = models.CharField(max_length=100)
    
    def __str__(self):
        return 'Project %s' % self.title