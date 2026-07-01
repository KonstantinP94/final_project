from django.shortcuts import render, redirect
from django.contrib.auth import login, logout

from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from datetime import date, timedelta

# Create your views here.


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('users:login')
        
    else:
        form = CustomUserCreationForm()   

    return render(request, 'register.html', context={'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('sport:home')
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('users:login')
    

from datetime import date, timedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def profile_view(request):
    all_bookings = request.user.bookings.select_related('slot', 'slot__trainer')

    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    period = request.GET.get('period', '')

    today = date.today()

    if period == 'today':
        date_from = today.isoformat()
        date_to = today.isoformat()
    elif period == 'week':
        date_from = today.isoformat()
        date_to = (today + timedelta(days=7)).isoformat()
    elif period == 'month':
        date_from = today.isoformat()
        date_to = (today + timedelta(days=30)).isoformat()

    upcoming = all_bookings.filter(slot__date__gte=today)
    past = all_bookings.filter(slot__date__lt=today)

    if date_from:
        upcoming = upcoming.filter(slot__date__gte=date_from)
        past = past.filter(slot__date__gte=date_from)
    if date_to:
        upcoming = upcoming.filter(slot__date__lte=date_to)
        past = past.filter(slot__date__lte=date_to)

    upcoming = upcoming.order_by('slot__date', 'slot__start_time')
    past = past.order_by('-slot__date', 'slot__start_time')

    total_bookings = all_bookings.count()

    return render(request, 'profile.html', {
        'upcoming_bookings': upcoming,
        'past_bookings': past,
        'total_bookings': total_bookings,
        'date_from': date_from,
        'date_to': date_to,
        'period': period,
        'has_bookings': all_bookings.exists(),
    })
