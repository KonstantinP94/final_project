from django.db import models

from datetime import date
from datetime import time
from datetime import datetime

from django.contrib.auth.models import User


class Trainer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    specialization = models.CharField(max_length=100)
    experience = models.PositiveIntegerField()
    photo = models.ImageField(upload_to='trainers', blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f'Имя: {self.first_name}, Фамилия: {self.last_name}'
    
    
class Slot(models.Model):
    trainer = models.ForeignKey(
        'Trainer',                
        on_delete=models.CASCADE, # каскадное удаление слотов при удалении тренера
        related_name='slots')     # чтобы можно было получить слоты тренера: trainer.slots.all()
    
    date = models.DateField(auto_now_add=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('trainer', 'date', 'start_time')
        
    def __str__(self):
        return f"Тренер: {self.trainer}, Дата: {self.date}, Время: {self.start_time}"
    
    
class Booking(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='bookings'   # user.bookings.all()
    )
    slot = models.OneToOneField(
        'Slot',
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    created_at = models.DateTimeField(auto_now_add=True)  # дата и время бронирования

    def __str__(self):
        return f"{self.user} – {self.slot}"
