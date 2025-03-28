from django.db import models

class Apartment(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='apartment_images', blank=True)
    description = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    rooms = models.IntegerField()
    bathrooms = models.IntegerField()
    extra_info = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class Arrival(models.Model):
    apartment = models.ForeignKey(Apartment, null=True, blank=True, on_delete=models.CASCADE)
    arrival_date = models.DateField()
    departure_date = models.DateField()

