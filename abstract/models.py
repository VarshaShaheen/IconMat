import threading

from django.db import models
from django.contrib.auth import get_user_model
from home.utils import send_html_email

# Create your models here.


MODE_OF_PRESENTATION = (
	('oral', 'Oral presentation (10 mint)'),
	('flash', 'Flash Presentation (5 mint)'),
	('poster', 'Poster Presentation'),
)


class PaperAbstract(models.Model):
	user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
	title = models.CharField(max_length=500)
	authors = models.CharField(max_length=500)
	abstract = models.TextField(blank=True, null=True)
	keywords = models.CharField(max_length=500, blank=True, null=True)
	file = models.FileField(upload_to='abstracts', null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	presentation = models.CharField(max_length=100, choices=MODE_OF_PRESENTATION, default='oral')

	def __str__(self):
		return self.title

	def send_email(self):
		context = {
			'subject'     : 'New Abstract Submitted',
			'content'     : f"New Abstract {self.title}, Submitted  by {self.user.first_name} {self.user.email} use the link to download the file https://localhost:8000{self.file.url} ",
			'user_name'    : self.user.first_name,
			'keywords'    : self.keywords,
			'file'        : self.file,
			'created_at'  : self.created_at,
			'updated_at'  : self.updated_at,
			'presentation': self.presentation,
		}
		threading.Thread(target=send_html_email, args=(context['subject'], self.user.email,context)).start()
