from django.db import models
from apartment.models import Apartment
from django.contrib.auth.models import User
from django.utils import timezone

cleaning_status = {
    ('A', 'assigned'),
    ('C', 'completed'),
    ('P', 'pending')
}

# Create your models here.
class Cleaning(models.Model):
    date = models.DateField()
    status = models.CharField(max_length=10, choices=cleaning_status, default='P')
    cleaner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    arrival_time = models.TimeField(null=True, blank=True)
    departure_time = models.TimeField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if self.cleaner is not None and self.status == 'P':
            self.status = 'A'
        
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