from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template import loader
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_html_email(subject, to_email, context):
	try:
		# Load the template
		html_template = loader.get_template('email/email_template.html')

		# Render the template with context
		html_content = html_template.render(context)

		# Strip the HTML content to create a plain text version
		text_content = strip_tags(html_content)

		# Create the email
		email = EmailMultiAlternatives(
			subject=subject,
			body=text_content,  # Plain text content for email clients that don't support HTML
			from_email=settings.EMAIL_HOST_USER,
			to=[to_email]
		)

		# Attach the HTML content as an alternative
		email.attach_alternative(html_content, "text/html")

		# Send the email
		email.send()
	except Exception as e:
		logger.error(f'Failed to send email to {to_email}: {e}')
		return False
	return True
