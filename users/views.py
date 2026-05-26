from django.shortcuts import render, redirect
from django.contrib.auth import login

from .forms import CustomUserCreationForm

# Create your views here.


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('sport:home')
        # если форма невалидна, то выходим из if и в конце render покажет форму с ошибками
    else:
        form = CustomUserCreationForm()   # пустая форма для GET

    return render(request, 'register.html', {'form': form})
