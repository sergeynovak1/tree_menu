from django.db import models


class MenuItem(models.Model):
    title = models.SlugField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='childrens')

    def __str__(self):
        return self.title
