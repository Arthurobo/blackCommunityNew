from django.db import models
from django.urls import reverse
from autoslug import AutoSlugField
from account.models import Profile

class Group(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=100, blank=True)
    follows = models.ManyToManyField(Profile, blank=True, related_name='group_follows')
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('group:group-detail-view', args=[str(self.id)])

    def get_group_follow_url(self):
        return reverse('group:group-follow-toggle', kwargs={'id': self.id})

    def get_group_follow_api_url(self):
        return reverse('group:group-follow-api-toggle', kwargs={'id': self.id})



class Post(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_posts', null=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='group_posts')
    content = models.TextField()
    likes = models.ManyToManyField(Profile, blank=True, related_name='group_post_likes')
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return str(self.content[:20])

    def get_absolute_url(self):
        return reverse('group:group-post-detail-view', args=[str(self.id)])

    def get_group_post_like_url(self):
        return reverse('group:group-post-like-toggle', kwargs={'id': self.id})

    def get_group_post_like_api_url(self):
        return reverse('group:group-post-like-api-toggle', kwargs={'id': self.id})