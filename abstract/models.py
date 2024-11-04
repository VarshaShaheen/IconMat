import threading

from django.db import models
from django.contrib.auth import get_user_model
from home.utils import send_html_email
from home.models import Symposia

# Create your models here.


MODE_OF_PRESENTATION = (
	('oral', 'Oral presentation (10 mint)'),
	('flash', 'Flash Presentation (5 mint)'),
	('poster', 'Poster Presentation'),
)

TITLE = (
	('Dr', 'Dr'),
	('Prof', 'Prof'),
	('Mr', 'Mr'),
	('Mrs', 'Mrs'),
	('Miss', 'Miss'),
	('Ms', 'Ms'),
)


class PaperAbstract(models.Model):
	user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
	title = models.CharField(max_length=10, choices=TITLE, default='Mr')
	name = models.CharField(max_length=100, default='')  # Removed the dynamic default
	phone_number = models.CharField(max_length=15)
	title_of_abstract = models.CharField(max_length=100)
	designation = models.CharField(max_length=100, default='')
	organization = models.CharField(max_length=100, default='')
	keywords = models.CharField(max_length=500, blank=True, null=True)
	symposia = models.ForeignKey(Symposia, on_delete=models.CASCADE)
	abstract = models.FileField(upload_to='abstracts')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	mode_of_presentation = models.CharField(max_length=100, choices=MODE_OF_PRESENTATION, default='oral')

	def save(self, *args, **kwargs):
		if not self.name and self.user:
			self.name = self.user.first_name  # Set name based on user's first name if not provided
		super().save(*args, **kwargs)

	def __str__(self):
		return self.title_of_abstract

	def send_email(self):
		context = {
			'subject'     : 'New Abstract Submitted',
			'content'     : f"New Abstract {self.title}, Submitted  by {self.user.first_name} {self.user.email} use the link to download the file https://iconmat2025{self.abstract.url} ",
			'user_name'   : self.user.first_name,
			'keywords'    : self.keywords,
			'file'        : self.file,
			'created_at'  : self.created_at,
			'updated_at'  : self.updated_at,
			'presentation': self.presentation,
		}
		threading.Thread(target=send_html_email, args=(context['subject'], self.user.email, context)).start()
