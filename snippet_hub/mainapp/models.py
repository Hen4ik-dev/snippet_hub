from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    bio = models.CharField(verbose_name= 'biography', help_text= 'bio')
    user = models.OneToOneField(User, on_delete= models.CASCADE, related_name= 'profile')

class Tag(models.Model):
    name = models.CharField(help_text= 'tag')

class Snippet(models.Model):
    content = models.TextField(blank= False, null= False, help_text='content')
    created_at = models.DateTimeField(auto_now_add= True)
    title = models.CharField(null= False, blank= False, help_text= 'title')
    author = models.ForeignKey(User, on_delete= models.CASCADE, related_name= 'snippets')
    tags = models.ManyToManyField(Tag, related_name= 'snippets', blank= True)
    language = models.CharField(default= 'html', null= False)
    is_private = models.BooleanField(default=True, )




