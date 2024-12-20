from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import User, Customer
from django.core.mail import send_mail
from django.conf import settings


@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    user = instance
    if created:
        customer = Customer.objects.create(
            user = user
        )
        subject = 'Welcome to emmanuel\'s website'
        message = 'we are glad you could make it'
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
    )
        
        
        
        
@receiver(post_delete, sender=Customer)
def delete_customer(sender, instance, **kwargs):
    user = instance.user
    user.delete()
    print('user associated with customer has been deleted')
    
    
    
    
    
        
    
    


