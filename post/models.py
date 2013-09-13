from django.db import models
from django.template.defaultfilters import slugify

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    text = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('post_detail', (), 
                {
                    'slug' :self.slug,
                })

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

class Comment(models.Model):
    name=models.CharField(max_length=100)
    email = models.EmailField(max_length=40)
    text = models.TextField()
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    created_on = models.DateTimeField(auto_now_add=True)
    #is_visible = models.NullBooleanField(default=True)

    def __unicode__(self):
        return self.text

