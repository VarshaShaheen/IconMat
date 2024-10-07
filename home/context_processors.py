# context_processors.py

from home.models import Social

def social(request):
    # Fetch the social media links from the database
    try:
        social_links = Social.objects.last()  # Assuming only one instance
    except Social.DoesNotExist:
        social_links = None  # Handle if no social links exist

    # Return the data in a dictionary that can be accessed in all templates
    return {
        'social_link_instagram': social_links.instagram,
	    'social_link_facebook': social_links.facebook,
	    'social_link_linkedin': social_links.linkedin
    }
