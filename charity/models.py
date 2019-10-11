from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


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
    description = models.TextField(null=True)
    type = models.SmallIntegerField(choices=ORGANIZATIONS, default=FUNDACJA)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name


class Donation(models.Model):
    quantity = models.SmallIntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=128)
    phone_number = models.IntegerField()
    city = models.CharField(max_length=128)
    zip_code = models.CharField(max_length=10)
    pick_up_date = models.DateField(null=True)
    pick_up_time = models.TimeField(null=True)
    pick_up_comment = models.TextField()
    user = models.ForeignKey(User, null=True, default=None, on_delete=models.CASCADE)
    is_taken = models.BooleanField(default=False)
