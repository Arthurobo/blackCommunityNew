from django.db import models
from django.urls import reverse
from autoslug import AutoSlugField
from account.models import Profile

class Group(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=100, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(Profile, related_name='group_likes')

    def total_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse('group:group-detail-view', args=[str(self.id)])

    def __str__(self):
        return self.name



class Post(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_posts', null=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='group_posts')
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return str(self.content[:20])