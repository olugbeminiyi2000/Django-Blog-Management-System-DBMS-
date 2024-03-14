from django.db import models

# Create your models here.
class Profiles(models.Model):
    email = models.EmailField(unique=True, null=False)
    password = models.CharField(max_length=80, unique=True, null=False)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "<email=%s, password=%s, date_created=%s>" % (self.email, self.password, self.date_created)
