from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Tasks(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_task')
    task = models.CharField(max_length=200)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created','-updated']

    def __str__(self):
        return self.task