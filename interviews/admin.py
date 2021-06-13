from django.contrib import admin

# Register your models here.
from .models import Person, Interview

admin.site.register(Person)
admin.site.register(Interview)