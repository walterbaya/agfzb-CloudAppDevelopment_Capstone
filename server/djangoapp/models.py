from django.db import models
from django.utils.timezone import now


# Create your models here.

# Create a Car Make model 

class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30, default='')
    description = models.CharField(null=False, max_length=30, default='')
    
    def __str__(self):
        return "Name: " + self.name + ", " + \
               "Description: " + self.description + ", " \

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

class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data

class DealerReview:
    
    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, id):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
        self.id = id

    def __str__(self):
        return "DealerShip reviewer name: " + self.name