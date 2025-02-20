from django.db import models
from apartment.models import Apartment
from django.contrib.auth.models import User

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
    
    def save(self, *args, **kwargs):
        if self.cleaner is not None:
            self.status = 'A'
        super(Cleaning, self).save(*args, **kwargs)
    
review_status = {
    ('C', 'checked'),
    ('I', 'issue_found'),
    ('N', 'not_checked')
}

class Review(models.Model):
    handyman = models.ForeignKey(User, on_delete=models.CASCADE)
    cleaning = models.ForeignKey(Cleaning, on_delete=models.CASCADE)
    date = models.DateTimeField()
    status = models.CharField(max_length=1, choices=review_status, default='N')
    comment = models.CharField(max_length=200)