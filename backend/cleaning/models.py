from django.db import models
from apartment.models import Apartment
from django.contrib.auth.models import User
from django.utils import timezone
from apartment.models import Arrival
from datetime import datetime
from notifications.utils import send_notification


cleaning_status = {
    ('A', 'assigned'),
    ('C', 'completed'),
    ('P', 'pending')
}

# Create your models here.
class Cleaning(models.Model):
    arrival = models.ForeignKey(Arrival, null=True, blank=True, on_delete=models.CASCADE) 
    status = models.CharField(max_length=10, choices=cleaning_status, default='P')
    cleaner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    arrival_time = models.TimeField(null=True, blank=True)
    departure_time = models.TimeField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if self.cleaner is not None and self.status == 'P':

            self.status = 'A'

            admins = User.objects.filter(profile__role='admin')

            send_notification(
                title=f"Cleaning assigned to {self.cleaner.username}",
                message=f"Cleaning assigned to {self.cleaner.username} for {self.apartment.name} ({self.arrival.departure_date})",
                django_user_ids=[admin.id for admin in admins]
            )

            send_notification(
                title="Limpieza pendiente para mañana",
                message=f"Preparate para limpiar el apartamento {self.apartment.name} ({self.arrival.departure_date}) mañana.",
                django_user_ids=[self.cleaner.id],
                scheduled_time=datetime.combine(self.arrival.departure_date, datetime.min.time().replace(hour=10))
            )

        admins = User.objects.filter(profile__role='admin')

        if self.status == 'C':
            send_notification(
                title=f"Cleaning completed",
                message=f"Cleaning completed for {self.apartment.name} ({self.arrival.departure_date})",
                django_user_ids=[admin.id for admin in admins]
            )
        
        super(Cleaning, self).save(*args, **kwargs)
        
        # Automatically create a Review when a Cleaning instance is created
        if not Review.objects.filter(cleaning=self).exists():
            Review.objects.create(
                cleaning=self,
                date=timezone.now(),
                status='N',
                comment=''
            )

review_status = {
    ('C', 'checked'),
    ('I', 'issue_found'),
    ('N', 'not_checked')
}

class Review(models.Model):
    handyman = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    cleaning = models.OneToOneField(Cleaning, on_delete=models.CASCADE, related_name='review')
    date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=1, choices=review_status, default='N')
    comment = models.CharField(max_length=200, blank=True)