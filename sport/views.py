from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Trainer, Slot, Booking, Review
from datetime import date
from django.db.models import Avg

def home(request):
    trainers = Trainer.objects.all()
    return render(request, 'home.html', {'trainers': trainers})



def trainer_detail(request, trainer_id):
    trainer = get_object_or_404(Trainer, id=trainer_id)
    slots = Slot.objects.filter(trainer=trainer)
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    show_only_free = request.GET.get('show_only_free')
    
    if date_from:
        slots = slots.filter(date__gte=date_from)
    if date_to:
        slots = slots.filter(date__lte=date_to)
    if show_only_free == 'on':
        slots = slots.filter(is_booked=False)
        
    today = date.today().isoformat()
    slots = slots.order_by('date', 'start_time')
    reviews = trainer.reviews.select_related('user').all()
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    
    user_review = None
    if request.user.is_authenticated:
        user_review = trainer.reviews.filter(user=request.user).first()
        
    return render(request, 'trainer_detail.html', {
        'trainer': trainer,
        'slots': slots,
        'date_from': date_from,
        'date_to': date_to,
        'show_only_free': show_only_free,
        'today': today,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'user_review': user_review,
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

@login_required
def add_review(request, trainer_id):
    trainer = get_object_or_404(Trainer, id=trainer_id)
    
    if request.method != 'POST':
        return redirect('sport:trainer_detail', trainer_id=trainer.id)
    
    if Review.objects.filter(trainer=trainer, user=request.user).exists():
        messages.error(request, 'Вы уже оставили отзыв на этого тренера.')
        return redirect('sport:trainer_detail', trainer_id=trainer.id)
    
    rating = request.POST.get('rating')
    text = request.POST.get('text', '').strip()
    
    if rating not in ['1', '2', '3', '4', '5'] or not text:
        messages.error(request, 'Пожалуйста, выберите оценку и напишите текст отзыва.')
        return redirect('sport:trainer_detail', trainer_id=trainer.id)
    
    Review.objects.create(
        trainer=trainer,
        user=request.user,
        rating=int(rating),
        text=text
    )
    
    messages.success(request, 'Спасибо за ваш отзыв!')
    return redirect('sport:trainer_detail', trainer_id=trainer.id)

@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    
    if request.method != 'POST':
        return redirect('sport:trainer_detail', trainer_id=review.trainer.id)
    
    rating = request.POST.get('rating')
    text = request.POST.get('text', '').strip()
    
    if rating not in ['1', '2', '3', '4', '5'] or not text:
        messages.error(request, 'Пожалуйста, выберите оценку и напишите текст отзыва.')
        return redirect('sport:trainer_detail', trainer_id=review.trainer.id)

    review.rating = int(rating)
    review.text = text
    review.save()

    messages.success(request, 'Ваш отзыв был обновлён!')
    return redirect('sport:trainer_detail', trainer_id=review.trainer.id)


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
     
    if request.method != 'POST':
        return redirect('sport:trainer_detail', trainer_id=review.trainer.id)

    trainer_id = review.trainer.id
    
    review.delete()

    messages.success(request, 'Ваш отзыв был удалён.')
    return redirect('sport:trainer_detail', trainer_id=trainer_id)

def about(request):
    return render(request, 'about.html')

def contacts(request):
    return render(request, 'contacts.html')