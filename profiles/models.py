# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd Party
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField
# Internal
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        primary_key=True
    )
    default_phone_number = models.CharField(max_length=20, blank=True, null=True)
    default_address1 = models.CharField(max_length=80, blank=True, null=True)
    default_address2 = models.CharField(max_length=80, blank=True, null=True)
    default_town_city = models.CharField(max_length=40, blank=True, null=True)
    default_county = models.CharField(max_length=80, blank=True, null=True)
    default_postcode = models.CharField(max_length=20, blank=True, null=True)
    default_country = CountryField(blank_label='Country', max_length=40, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"


#  Create profile or save if already exists
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create / update the user profile
    """
    if created:
        UserProfile.objects.create(user=instance)
        instance.userprofile.save()