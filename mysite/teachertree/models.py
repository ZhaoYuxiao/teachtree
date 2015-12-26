#-*- coding:utf-8 -*-
from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    sex = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    school = models.CharField(max_length=100)
    email = models.EmailField()
    province = models.CharField(max_length=100)
    identity_card = models.CharField(max_length=18)
    def __unicode__(self):
        return self.name


class Teacher(models.Model):
    pid = models.ForeignKey(Person)
    tid = models.IntegerField()
    date0 = models.DateField()
    date1 = models.DateField()
    def __unicode__(self):
        return self.tid
 
        
class Student(models.Model):
    pid = models.ForeignKey(Person)
    sid = models.IntegerField()
    date0 = models.DateField()
    date1 = models.DateField()
 
