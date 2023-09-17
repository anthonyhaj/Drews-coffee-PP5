from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    friendly_name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name
