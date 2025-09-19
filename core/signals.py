from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
User = get_user_model()
@receiver(post_save, sender=User)
def send_activation_email(sender, instance, created, **kwargs):
    if created:
        token = default_token_generator.make_token(instance)
        activation_url = f"https://demo.likhon.com.bd/ems/users/activate/{instance.id}/{token}"
        subject = "Active your event management system account"
        message = f"Hi, {instance.username} \n \n Please active your account. by clicking the link : {activation_url} \n \n Thank You"
        reciepientlist = [instance.email]
        try:
            send_mail(subject, message, "no_reply@likhon.com.bd", reciepientlist)
        except Exception as e:
            print(f"Failed to send email to {instance.email}: {str(e)}")

@receiver(post_save, sender=User)
def assign_role(sender, instance, created, **kwargs):
    if created:
        user_group, created = Group.objects.get_or_create(name='User')
        instance.groups.add(user_group)
        instance.save()