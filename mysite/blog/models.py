from django.conf import settings
from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.

class PublishedManager(models.Manager):
    def get_queryset(self):
        return (
            super().get_queryset().filter(status=Post.Status.PUBLISHED)
        )

"""
    Every model is translated to db table, in this case by de app blog each model will added flag blog_ in the name,
    for example blog_post table.
"""

class Post(models.Model):

    # enumeration Class
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
    
    title = models.CharField(max_length=250)
    """
        slug is used by SEO friendly, for example django-renhardt-legend-jazz
    """
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    
    # auto_now_add store the date and time when the post was created
    
    created = models.DateTimeField(auto_now_add=True)

    # auto_now store th last date and time when the post was updated
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=Status,
        default=Status.DRAFT
    )

    # many-to-one relationship
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_post'
    )

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    # keep the default objects manager
    objects = models.Manager() # Default manager (objects)
    published = PublishedManager() # Our custom manager


    """
        Django use this method to display the name of the object in mane places,
        such as the Django
    """
    def __str__(self) -> str:
        return self.title
    
    # Using canocial URL

    def get_absolute_url(self):
        return reverse(
            'blog:post_detail',
            args=[self.id]
        )
