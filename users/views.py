from django.shortcuts import render, redirect
from django.contrib.auth import login, logout

from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
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
    
@login_required
def profile_view(request):
    
    bookings = (request.user.bookings
                .select_related('slot__trainer')
                .order_by('slot__start_time'))
    return render(request, 'profile.html', {'bookings': bookings})