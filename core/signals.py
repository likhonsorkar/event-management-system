from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

@receiver(post_save, sender=User)
def handle_user_registration(sender, instance, created, **kwargs):
    """
    Handle new user registration:
    1. Assign 'participant' role.
    2. Set inactive.
    3. Send activation email using settings for domain/protocol.
    """
    if created:
        # 1. Assign participant role
        participant_group, _ = Group.objects.get_or_create(name='participant')
        instance.groups.add(participant_group)
        
        # 2. Handle activation for non-staff/non-superusers
        if not instance.is_staff and not instance.is_superuser:
            # Set inactive
            User.objects.filter(pk=instance.pk).update(is_active=False)
            
            # 3. Send activation email
            token = default_token_generator.make_token(instance)
            uid = urlsafe_base64_encode(force_bytes(instance.pk))
            
            # Use settings configured with decouple
            domain = settings.SITE_DOMAIN
            protocol = settings.SITE_PROTOCOL
            
            subject = "Activate Your Account"
            context = {
                'user': instance,
                'domain': domain,
                'uid': uid,
                'token': token,
                'protocol': protocol,
            }
            
            message = render_to_string('activation_email.html', context)
            
            email = EmailMultiAlternatives(subject, "", to=[instance.email])
            email.attach_alternative(message, "text/html")
            try:
                email.send()
            except Exception as e:
                # Log error in production
                print(f"Error sending activation email: {e}")
