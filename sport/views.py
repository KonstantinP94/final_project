from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Trainer, Slot, Booking

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
    

    
@login_required
def book_slot(request, slot_id):

    slot = get_object_or_404(Slot, id=slot_id)


    if slot.is_booked:
        messages.error(request, 'Этот слот уже занят. Выберите другое время.')
        return redirect('sport:trainer_detail', trainer_id=slot.trainer.id)

    
    booking = Booking.objects.create(
        user=request.user,
        slot=slot
    )

    slot.is_booked = True
    slot.save()

    messages.success(request, f'Вы успешно записаны на занятие к {slot.trainer} на {slot.start_time}')

    return redirect('users:profile')


@login_required
def cancel_booking(request, booking_id):
    
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    
    slot = booking.slot
    slot.is_booked = False
    slot.save()
    
    
    booking.delete()
    
    
    messages.success(request, f'Запись на {slot.start_time} отменена.')
    
    
    return redirect('users:profile')