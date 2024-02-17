from django.db import models
from django.utils.text import slugify


class MenuItem(models.Model):
    title = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='childrens')
    url = models.SlugField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        if not self.url:
            self.url = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
