from django.db import models
# from django.core.validators import FileExtensionValidator
# from account.models import Profile
# from django.shortcuts import reverse


class Post(models.Model):
    name = models.CharField(max_length=200)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)

    class Meta:
        ordering = ('-created',)