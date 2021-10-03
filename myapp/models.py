from django.db import models


class Prediction(models.Model):
    path = models.CharField(max_length=50)
    prediction = models.IntegerField()
    long = models.CharField(max_length=100)
    lat=models.CharField(max_length=100)
# Create your models here.
class Car(models.Model):
    name = models.CharField(max_length=100)
    top_speed = models.IntegerField()