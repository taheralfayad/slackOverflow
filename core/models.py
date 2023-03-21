from django.db import models

# Create your models here.
class Card(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=250)
    author = models.CharField(max_length=100)
    project = models.CharField(max_length=100, null=True)

    def __str__(self):
        return 'Card for %s' % self.project

    def __repr__(self):
        return '<Card: %r>' % self.project

