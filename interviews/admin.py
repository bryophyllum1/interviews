from django.contrib import admin

# Register your models here.
from .models import Interviewee, Interviewer, Interview

admin.site.register(Interviewee)
admin.site.register(Interviewer)
admin.site.register(Interview)