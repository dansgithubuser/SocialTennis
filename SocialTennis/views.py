from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
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
    friends = models.Friend.objects.filter(user_id=request.user.id).order_by('id')
    return render(request, 'home.html', {'friends': friends})

def friend(request):
    models.Friend.objects.create(
        user_id=request.user.id,
        name=request.POST['name'],
    )
    return redirect('/home')
