from django.db import models
from django.utils import timezone
# Create your models here.


def add_an_hour():
    return timezone.now() + timezone.timedelta(hours=1)


class Person(models.Model):
    name = models.CharField(blank=False, null=False, max_length=500)
    email = models.EmailField(blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Interviewer(Person):
    pass


class Interviewee(Person):
    pass


class Interview(models.Model):
    interviewer = models.ManyToManyField(Interviewer, blank=False, related_name='interviewer')
    interviewee = models.ManyToManyField(Interviewee, blank=False, related_name='interviewee')
    start_datetime = models.DateTimeField(default=timezone.now, blank=False, null=False)
    end_datetime = models.DateTimeField(default=add_an_hour, blank=False, null=False)
    more_info = models.TextField(blank=True, null=False, default="", max_length=500)

    def __str__(self):
        if self.start_datetime.date() == self.end_datetime.date():
            return f"Interview from {self.start_datetime.strftime('%-I:%M %p')} to {self.end_datetime.strftime('%-I:%M %p')} on {self.start_datetime.strftime('%-d %b, %y')}"
        else:
            return f"Interview from {self.start_datetime.date()} to {self.end_datetime.date()}"

    def is_conflicting(self):
        allInterviews = Intervew.objects.al()
        for interview in allInterviews:
            isdt = interview.start_datetime
            iedt = interview.end_datetime

            if ((self.start_datetime < isdt and self.end_datetime <= isdt)\
                    or (self.start_datetime >= iedt and self.end_datetime > iedt)):
                return True
            return False