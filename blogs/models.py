from django.db import models
from ckeditor.fields import RichTextField
from django import forms

"""Blogify Blogs Models"""
class Image(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    creation = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class ImageForm(forms.ModelForm):    
    class Meta:
        model = Image
        fields = ('title', 'image')

class Blog(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=400)
    body = RichTextField(blank=True)
    author = models.CharField(max_length=50)
    image = models.ForeignKey(Image, on_delete=models.RESTRICT,blank=True,null=True)
    creation = models.DateTimeField(auto_now=True)
    
    def __str__(self):
       return f"""
        Title: {self.title[0:20]}
        Body: {self.body[0:50]}
        Author: {self.author}
       """

class Page(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField(blank=True)
    image = models.ForeignKey(Image, on_delete=models.RESTRICT,blank=True,null=True)
    
    def __str__(self):
        return f"""
            Title: {self.title[0:10]}
            Content: {self.content[0:50]}
        """