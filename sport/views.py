from django.shortcuts import render, get_object_or_404
from .models import Trainer, Slot  

def home(request):
    trainers = Trainer.objects.all()          
    return render(request, 'home.html', {'trainers': trainers})



def trainer_detail(request, trainer_id):

    trainer = get_object_or_404(Trainer, id=trainer_id)
 
    slots = Slot.objects.filter(trainer=trainer)
    
    slots = slots.order_by('start_time')
    
    return render(request, 'trainer_detail.html', {
        'trainer': trainer,
        'slots': slots,
    })