from django.shortcuts import render, get_object_or_404
from .models import Trainer, Slot   # импортируем модель Trainer

def home(request):
    trainers = Trainer.objects.all()          # получаем всех тренеров
    return render(request, 'home.html', {'trainers': trainers})



def trainer_detail(request, trainer_id):
    # 1. Получаем тренера по id или 404
    trainer = get_object_or_404(Trainer, id=trainer_id)
    
    # 2. Получаем все слоты этого тренера
    slots = Slot.objects.filter(trainer=trainer)
    
    # 3. Сортируем слоты по дате и времени начала (по возрастанию)
    slots = slots.order_by('start_time')
    
    # 4. Рендерим шаблон с контекстом
    return render(request, 'trainer_detail.html', {
        'trainer': trainer,
        'slots': slots,
    })