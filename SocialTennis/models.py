from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

def choicify(*args): return [(i, i) for i in args]

class Friend(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    name = models.TextField()

class Event(models.Model):
    SERVER_CHOICES = choicify('me', 'them', 'neither')
    KIND_CHOICES = choicify('plan', 'meet')

    friend = models.ForeignKey('Friend', models.CASCADE)
    server = models.TextField(choices=SERVER_CHOICES)
    kind = models.TextField(choices=KIND_CHOICES)
    note = models.TextField(null=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
