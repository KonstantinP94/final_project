from django.db import models

from datetime import date
from datetime import time
from datetime import datetime

from django.contrib.auth.models import User

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Booking  


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
        on_delete=models.CASCADE, 
        related_name='slots')     
    
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
        related_name='bookings'  
    )
    slot = models.OneToOneField(
        'Slot',
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} – {self.slot}"


@receiver(post_save, sender=Booking)
def mark_slot_booked(sender, instance, created, **kwargs):
    if created:
        instance.slot.is_booked = True
        instance.slot.save()
        

@receiver(post_delete, sender=Booking)
def mark_slot_free(sender, instance, **kwargs):
    instance.slot.is_booked = False
    instance.slot.save()