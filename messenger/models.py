from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Chat(models.Model):    
    sender = models.CharField(max_length=100)
    receiver = models.CharField(max_length=100)
    text = models.CharField(max_length=100)
    status = models.CharField(max_length=10,null=True)
    creation = models.DateTimeField(auto_now=True)    

    def __str__(self):
        return f"""
            {self.sender} 
            to: {self.receiver}
            text: {self.text[0:8]}...
            status. {self.status}
            creation: {self.creation}
        """
