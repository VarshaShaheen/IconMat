from django.db import models

# Create your models here.


class People(models.Model):

	DESIGNATION = (
		('Conference Chair','Conference Chair'),
		('Conference Patron','Conference Patron'),
	)

	name = models.CharField(max_length=100)
	email = models.EmailField(max_length=100,null=True,blank=True)
	phone = models.CharField(max_length=15,default='Not Provided',null=True,blank=True)
	message = models.TextField(default='Not Provided',null=True,blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	image = models.ImageField(upload_to='people',null=True,blank=True)
	designation = models.CharField(max_length=100,choices=DESIGNATION,default='Not Provided',null=True,blank=True)

	def __str__(self):
		return self.name