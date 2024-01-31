from django.db import models
from django.utils.timezone import now


# Create your models here.

# Create a Car Make model 

class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30, default='')
    description = models.CharField(null=False, max_length=30, default='')
    
    def __str__(self):
        return "Name: " + self.name + ", " + \
               "Type: " + self.type + ", " \
               "Year: " + str(self.year)

# Create a Car Model model 
class CarModel(models.Model):
    SEDAN = 'Sedan'
    WAGON = 'Wagon'
    SUV = 'Suv'
    TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (WAGON, 'Wagon'),
        (SUV, 'Suv'),
    ]

    name = models.CharField(null=False, max_length=30, default='')

    field = models.ForeignKey('CarMake', on_delete=models.CASCADE)

    dealer_id = models.IntegerField()

    type =  models.CharField(
        null=False,
        max_length=20,
        choices=TYPE_CHOICES,
        default=SEDAN
    )

    year = models.DateField(null=True)
    
    def __str__(self):
        return "Name: " + self.name + ", " + \
                "Type: " + self.type + ", " \
                "Year: " + str(self.year) 

# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
