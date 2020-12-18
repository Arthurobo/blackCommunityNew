from django.db import models
from django.urls import reverse
from autoslug import AutoSlugField
from account.models import Profile

class Page(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, unique=True)
    slug = AutoSlugField(populate_from='title', unique=True)
    likes = models.ManyToManyField(Profile, blank=True, related_name='page_likes')
    description = models.CharField(max_length=100, blank=True)
    country_location = models.CharField(max_length=100, blank=True)
    city_location = models.CharField(max_length=100, blank=True)
    ip_address = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=100, blank=True)
    business_email = models.CharField(max_length=100, blank=True)
    business_website = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=100, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('page:page-detail-view', kwargs={'slug': self.slug})

    def get_page_like_url(self):
        return reverse("page:page-like-toggle", kwargs={'slug': self.slug})

    def get_page_like_api_url(self):
        return reverse('page:page-like-api-toggle', kwargs={"slug": self.slug})


class Post(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='posts', null=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='page_posts')
    content = models.TextField()
    likes = models.ManyToManyField(Profile, blank=True, related_name='page_post_likes')
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_created']

    # Total comments count for a particular post
    def total_number_of_comments(self):
        return self.comment_set.all().count()

    def __str__(self):
        return str(self.content[:20])

    def get_absolute_url(self):
        return reverse("page:page-post-detail-view", args=[str(self.id)])
    
    def get_page_post_like_url(self):
        return reverse('page:page-post-like-toggle', kwargs={'id': self.id})

    def get_page_post_like_api_url(self):
        return reverse("page:page-post-like-api-toggle", kwargs={'id': self.id})


class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='page_post_comment_user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField(max_length=300)
    likes = models.ManyToManyField(Profile, blank=True, related_name='page_post_comment_likes')
    last_updated = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.body[:20])

    def get_absolute_url(self):
        return reverse("page:page-post-comment-detail-view", args=[str(self.id)])
    
    def get_page_post_comment_like_url(self):
        return reverse("page:page-post-comment-like-toggle", kwargs={'id': self.id})

    def get_page_post_comment_like_api_url(self):
        return reverse("page:page-post-comment-like-api-toggle", kwargs={'id': self.id})