from django.db import models


# Create your models here.


class People(models.Model):
	DESIGNATION = (
		('Conference Chair', 'Conference Chair'),
		('Conference Patron', 'Conference Patron'),
	)

	name = models.CharField(max_length=100)
	email = models.EmailField(max_length=100, null=True, blank=True)
	phone = models.CharField(max_length=15, default='Not Provided', null=True, blank=True)
	message = models.TextField(default='Not Provided', null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	image = models.ImageField(upload_to='people', null=True, blank=True)
	designation = models.CharField(max_length=100, choices=DESIGNATION, default='Not Provided', null=True, blank=True)
	priority = models.IntegerField(default=0)

	def __str__(self):
		return self.name


class Symposia(models.Model):
	title = models.CharField(max_length=100)
	author = models.CharField(max_length=100, null=True, blank=True)
	abstract = models.TextField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	image = models.ImageField(upload_to='synopsys', null=True, blank=True)

	def __str__(self):
		return self.title


class Carousel(models.Model):
	title = models.CharField(max_length=100, null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	image = models.ImageField(upload_to='carousel', null=True, blank=True)

	def __str__(self):
		return self.title


class Program(models.Model):
	title = models.CharField(max_length=100)
	description = models.TextField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title


class Speaker(models.Model):
	name = models.CharField(max_length=100)
	designation = models.CharField(max_length=100, default='', null=True, blank=True)
	email = models.EmailField(max_length=100, null=True, blank=True)
	phone = models.CharField(max_length=15, default='Not Provided', null=True, blank=True)
	message = models.TextField(default='Not Provided', null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	image = models.ImageField(upload_to='speakers', null=True, blank=True)
	priority = models.IntegerField(default=0)

	def __str__(self):
		return self.name


class AdvisoryCommittee(models.Model):
	name = models.CharField(max_length=100)
	email = models.EmailField(max_length=100, null=True, blank=True)
	phone = models.CharField(max_length=15, default='', null=True, blank=True)
	designation = models.CharField(max_length=100, default='', null=True, blank=True)
	message = models.TextField(default='', null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	image = models.ImageField(upload_to='advisory', null=True, blank=True)
	priority = models.IntegerField(default=0)

	def __str__(self):
		return self.name


class LocalOrganisingCommittiee(models.Model):
	name = models.CharField(max_length=100)
	email = models.EmailField(max_length=100, null=True, blank=True)
	phone = models.CharField(max_length=15, default='', null=True, blank=True)
	designation = models.CharField(max_length=100, default='', null=True, blank=True)
	message = models.TextField(default='', null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	image = models.ImageField(upload_to='advisory', null=True, blank=True)
	priority = models.IntegerField(default=100)

	def __str__(self):
		return self.name


class Social(models.Model):
	instagram = models.URLField(max_length=100, null=True, blank=True)
	linkedin = models.URLField(max_length=100, null=True, blank=True)
	facebook = models.URLField(max_length=100, null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return 'Social Links'


class Notification(models.Model):
	notification = models.CharField(max_length=50, null=True, blank=True)
	link = models.URLField(max_length=100, null=True, blank=True)

	def __str__(self):
		return str(self.notification)

class Settings(models.Model):
	pass



class Dates(models.Model):
	abstract_submission_start_date = models.DateField()
	abstract_submission_end_date = models.DateField()

	acceptance_of_abstract = models.DateField()

	early_bird_registration_start = models.DateField()
	early_bird_registration_end = models.DateField()

	full_paper_submission_deadline = models.DateField()
	spot_registration_for_indian_students_and_faculties = models.DateField()

	event_start_date = models.DateField()
	event_end_date = models.DateField()

	def __str__(self):
		return str(self.id)


class TouristAttraction(models.Model):
	title = models.CharField(max_length=150)
	description = models.TextField()
	image1 = models.ImageField(upload_to='tourist_attractions', null=True, blank=True)
	image2 = models.ImageField(upload_to='tourist_attractions', null=True, blank=True)
	image3 = models.ImageField(upload_to='tourist_attractions', null=True, blank=True)
	distance_from_cusat = models.FloatField(null=True,blank=True)
	location = models.URLField(null=True, blank=True)
	source = models.URLField(null=True,blank=True)

	def __str__(self):
		return self.title

