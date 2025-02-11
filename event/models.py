from django.db import models
from datetime import datetime


# Create your models here.


class Participant(models.Model):
    iconmat_id = models.CharField(max_length=10)
    name = models.CharField(max_length=100,blank=True,null=True)
    category = models.CharField(max_length=100,blank=True,null=True)
    presentation_id = models.CharField(max_length=10,blank=True, null=True)
    institution = models.CharField(max_length=100,blank=True,null=True)
    email = models.CharField(max_length=100,blank=True,null=True)
    registration_id = models.CharField(max_length=10,blank=True, null=True)
    amount_paid = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return str(self.iconmat_id + " " + self.name)




class CheckIn(models.Model):
    participant = models.OneToOneField(Participant, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.participant.iconmat_id + " " + self.participant.name + " " + str(self.timestamp.strftime('%Y-%m-%d %H:%M:%S')))


class Lunch(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.participant.iconmat_id + " " + self.participant.name + " " + str(
            self.timestamp.strftime('%Y-%m-%d %H:%M:%S')))


class Dinner(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.participant.iconmat_id + " " + self.participant.name + " " + str(
            self.timestamp.strftime('%Y-%m-%d %H:%M:%S')))