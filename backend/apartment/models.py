from django.db import models

class Apartment(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    rooms = models.IntegerField()
    bathrooms = models.IntegerField()
    extra_info = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name