from django.db import models
from django.core.validators import FileExtensionValidator
from account.models import Profile
from django.shortcuts import reverse


class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    #liked = models.ManyToManyField(Profile, blank=True, related_name='likes')
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.content[:20])

    # def num_likes(self):
    #     return self.liked.all().count()

    
    # def get_absolute_url(self):
    #     return reverse('post:post-detail-view')


# LIKE_CHOICES = (
#     ('Like', 'Like'),
#     ('Unlike', 'Unlike'),
# )

# class Like(models.Model): 
#     user = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     value = models.CharField(choices=LIKE_CHOICES, max_length=8)
#     updated = models.DateTimeField(auto_now=True)
#     created = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return f"{self.user}-{self.post}-{self.value}"

