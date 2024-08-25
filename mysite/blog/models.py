from django.db import models
from django.utils import timezone

# Create your models here.

"""
    Every model is translated to db table, in this case by de app blog each model will added flag blog_ in the name,
    for example blog_post table.
"""

class Post(models.Model):
    title = models.CharField(max_length=250)
    """
        slug is used by SEO friendly, for example django-renhardt-legend-jazz
    """
    slug = models.SlugField(max_length=250)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    
    # auto_now_add store the date and time when the post was created
    
    created = models.DateTimeField(auto_now_add=True)

    # auto_now store th last date and time when the post was updated
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    """
        Django use this method to display the name of the object in mane places,
        such as the Django
    """
    def __str__(self) -> str:
        return self.title
