from django.shortcuts import render
from .models import Trainer   # импортируем модель Trainer

def home(request):
    trainers = Trainer.objects.all()          # получаем всех тренеров
    return render(request, 'home.html', {'trainers': trainers})