# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class Contact(models.Model):
    """
    Model to store contact information and messages
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="contact_user",
        null=True
        )
    contact_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=True)
    email = models.EmailField(max_length=50, default="")
    phone = PhoneNumberField(null=True, blank=True)
    message = models.TextField(null=True)

    def __str__(self):
        return self.name
        