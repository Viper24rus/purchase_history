from django.db import models
from django.core.validators import DecimalValidator


class Customer(models.Model):
    username = models.CharField(max_length=20, primary_key=True)
    spent_money = models.DecimalField(max_digits=9,
                                      decimal_places=0,
                                      default=0,
                                      validators=[DecimalValidator(max_digits=9,
                                                                   decimal_places=0)])

    def __str__(self):
        return self.username


class Gem(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    customers = models.ManyToManyField(Customer, related_name='gems')

    def __str__(self):
        return self.name
