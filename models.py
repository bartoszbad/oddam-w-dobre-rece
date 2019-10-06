from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=128)


class Institution(models.Model):

    FUNDACJA = 0
    ORGANIZACJA_POZARZADOWA = 1
    ZBIORKA_LOKALNA = 2

    ORGANIZATIONS = (
        (FUNDACJA, 'fundacja'),
        (ORGANIZACJA_POZARZADOWA, 'organizacja pozarządowa'),
        (ZBIORKA_LOKALNA, 'zbiórka lokalna'),
    )

    name = models.CharField(max_length=128)
    description = models.TextField
    type = models.SmallIntegerField(choices=ORGANIZATIONS, default=FUNDACJA)
    categories = models.ManyToManyField(Category)


class Donation(models.Model):
    quantity = models.SmallIntegerField
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=128)
    phone_number = models.IntegerField
    city = models.CharField(max_length=128)
    zip_code = models.CharField(max_length=10)
    pick_up_date = models.DateField()
    pick_up_time = models.DateTimeField
    pick_up_comment = models.TextField
    user = models.ForeignKey(User, null=True, default=None, on_delete=models.CASCADE)
