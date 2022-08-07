from django.db import models

# Create your models here.
# Account models

from django.contrib.auth.models import User

from blogs.models import Image

class Profile(models.Model):    
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    description = models.CharField(max_length=400,null=True)
    image = models.ForeignKey(Image, on_delete=models.RESTRICT,blank=True,null=True)
    url_site = models.CharField(max_length=200,null=True)

    def __str__(self):
        return f"""
            User: {self.user}
            Description: {self.description[0:20]}
            Url_site: {self.url_site}
        """