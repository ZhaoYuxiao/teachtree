from django.db import models

# Create your models here.

class Person(models.Model):
    Teacher = models.ManyToManyField('self',symmetrical=False,related_name='t+')
    Name = models.CharField(max_length=100)
    Date = models.ManyToManyField('Time')
    Student = models.ManyToManyField('self',symmetrical=False,related_name='s+')
    def __unicode__(self):
        return self.Name
class Time(models.Model):
    Tors= models.ForeignKey(Person)
    Day = models.CharField(max_length=100)
    def __unicode__(self):
        return self.Day