from django.db import models
from apartment.models import Apartment
from django.contrib.auth.models import User

# Create your models here.
class Cleaning(models.Model):
    date = models.DateTimeField()
    status = models.CharField(max_length=10)
    cleaner = models.ForeignKey(User, on_delete=models.CASCADE)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    
review_status = {
    'C': 'checked',
    'I': 'issue_found'
}

class Review(models.Model):
    handyman = models.ForeignKey(User, on_delete=models.CASCADE)
    cleaning = models.ForeignKey(Cleaning, on_delete=models.CASCADE)
    date = models.DateTimeField()
    status = models.CharField(max_length=1, choices=[(key, value) for key, value in review_status.items()])
    comment = models.CharField(max_length=200)