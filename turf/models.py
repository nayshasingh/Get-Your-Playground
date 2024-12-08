from django.db import models
from datetime import date
# Create your models here.

class Contact(models.Model):
    yourName = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    mobilenumber = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.yourName


# Updated TurfBooked model for tracking bookings for a specific date and slot


class TurfBooked(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    amount = models.IntegerField()
    selected_date = models.DateField()  # Changed to DateField for better date handling
    booking_date = models.DateField(default=date.today)  # Default set to today's date
    booking_time = models.CharField(max_length=200, default="")  # Time of the booking (e.g., "10:00 AM")
    slots = models.JSONField(default=list)  # Storing booked slots as a list of slot identifiers or times

    
    def __str__(self):
        return f"{self.name} - {self.selected_date} - {self.booking_time}"
