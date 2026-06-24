from django.contrib import admin
from .models import Trainer, Slot, Booking, Review

admin.site.register(Trainer)
admin.site.register(Slot)
admin.site.register(Booking)
admin.site.register(Review)

