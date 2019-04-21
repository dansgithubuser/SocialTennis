from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Friend(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    name = models.TextField()

class Event(models.Model):
    friend = models.ForeignKey('Friend', models.CASCADE)
    server = models.TextField(choices=[('user', 'user'), ('friend', 'friend'), ('neither', 'neither')])
    created_at = models.DateTimeField()
