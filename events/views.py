from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import Event, Participant
from .forms import RegisterForm

def home(request):
    events = Event.objects.all().order_by('date')
    return render(request, 'events/home.html', {'events': events})

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    is_registered = False
    if request.user.is_authenticated:
        is_registered = Participant.objects.filter(event=event, user=request.user).exists()
    return render(request, 'events/event_detail.html', {
        'event': event,
        'is_registered': is_registered
    })

@login_required
def register_for_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    # Проверяем, не записан ли уже
    if Participant.objects.filter(event=event, user=request.user).exists():
        return redirect('event_detail', event_id=event_id)
    
    # Проверяем лимит участников
    if event.max_participants > 0 and event.participants.count() >= event.max_participants:
        return redirect('event_detail', event_id=event_id)
    
    # Записываем
    Participant.objects.create(event=event, user=request.user)
    return redirect('event_detail', event_id=event_id)

@login_required
def my_events(request):
    my_participations = Participant.objects.filter(user=request.user)
    return render(request, 'events/my_events.html', {'participations': my_participations})

# Функция регистр 
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматически входим после регистр
            return redirect('home')
    else:
        form = RegisterForm()
    
    return render(request, 'registration/register.html', {'form': form})
