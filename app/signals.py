from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *



@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        print("TRUER")
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    print("HI")
    instance.userprofile.save()
