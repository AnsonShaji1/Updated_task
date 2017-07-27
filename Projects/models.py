
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User



class Post(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=2000)
    text = models.TextField(max_length=100000)

    def __unicode__(self):
        return str(self.title)


class PermissionAdmin(models.Model):
	author = models.CharField(max_length=2000)
	per_read = models.BooleanField(default=False)
	per_edit = models.BooleanField(default=False)
	per_delete = models.BooleanField(default=False)
	per_create = models.BooleanField(default=False)

	def __unicode__(self):
		return str(self.author)


