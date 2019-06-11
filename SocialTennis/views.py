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
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def home(request):
    context = {}
    if request.user.id:
        friends = models.Friend.objects.filter(user_id=request.user.id).select_related()
        # friends listing
        context['friends'] = {}
        for friend in friends:
            friend.events = sorted(friend.event_set.all(), key=lambda i: i.date)[-5:]
            context['friends'][friend.id] = {
                'name': friend.name,
                'events': [{
                    'server': i.server,
                    'kind': i.kind,
                    'date': i.date.strftime('%Y-%m-%d'),
                } for i in friend.events],
            }
        # choices
        context['servers'] = models.Event.SERVER_CHOICES
        context['kinds'] = models.Event.KIND_CHOICES
        # recent events
        fortnight_ago = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=14)
        events = [j for i in friends for j in i.event_set.all()]
        context['recently_created_events'] = sorted([i for i in events if i.created_at > fortnight_ago       ], key=lambda i: i.created_at, reverse=True)
        context['recent_events'          ] = sorted([i for i in events if i.date       > fortnight_ago.date()], key=lambda i: i.date      , reverse=True)
        # ranking
        def score(friend):
            friend.score = 0
            if friend.events:
                server = friend.events[0].server
                date = friend.events[0].date
                class Today:
                    def __init__(self):
                        self.date = datetime.date.today()
                        self.server = None
                for i in friend.events[1:] + [Today()]:
                    days = (i.date - date).days
                    if server == 'me':
                        friend.score -= days
                    elif server == 'them':
                        friend.score += days
                    server = i.server
                days_since_contact = (datetime.date.today() - friend.events[-1].date).days
                if days_since_contact > 180:
                    friend.score += 2 * (days_since_contact - 180)
            print(friend.name, friend.score)
            return friend
        context['ranked'] = sorted([score(i) for i in friends], key=lambda i: i.score, reverse=True)
    return render(request, 'home.html', context)

def friend(request):
    models.Friend.objects.create(
        user_id=request.user.id,
        name=request.POST['name'],
    )
    return redirect('/')

def event(request):
    for friend_id in request.POST.getlist('friend'):
        if models.Friend.objects.get(id=friend_id).user_id != request.user.id:
            return HttpResponse(status=403)
        models.Event.objects.create(
            friend_id=int(friend_id),
            server=request.POST['server'],
            kind=request.POST['kind'],
            date=datetime.date(*[int(i) for i in request.POST['date'].split('-')]),
            note=request.POST.get('note'),
        )
    return redirect('/')
