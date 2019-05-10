import datetime
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from . import models

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def home(request):
    friends = models.Friend.objects.filter(user_id=request.user.id).select_related().order_by('id')
    return render(request, 'home.html', {'friends': friends})

def friend(request):
    models.Friend.objects.create(
        user_id=request.user.id,
        name=request.POST['name'],
    )
    return redirect('/home')

def event(request, server, friend_id):
    if models.Friend.objects.get(id=friend_id).user_id != request.user.id:
        return HttpResponse(status=403)
    models.Event.objects.create(
        friend_id=friend_id,
        server=server,
        kind=request.POST.get('kind'),
        created_at=datetime.datetime.now() - datetime.timedelta(days=int(request.POST['days_ago'])),
    )
    return redirect('/home')
