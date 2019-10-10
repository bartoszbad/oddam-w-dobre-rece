from django.contrib import admin
from charity.models import Category, Institution, Donation


# Register your models here.
admin.site.register(Category)
admin.site.register(Institution)
admin.site.register(Donation)