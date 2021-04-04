from django.db import models

# Create your models here.


class Building(models.Model):
    name = models.CharField(max_length=255)


class Meter(models.Model):
    # METER_TYPE = (
    #     ("G", "Natural Gass"),
    #     ("E", "Electricity"),
    #     ("W", "Water"),
    # )
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    fuel = models.CharField(max_length=25)
    unit = models.CharField(max_length=25)


class Consumption(models.Model):
    reading_date_time = models.DateTimeField(auto_now_add=True)
    meter = models.ForeignKey(Meter, on_delete=models.CASCADE)
    consumption = models.FloatField()
