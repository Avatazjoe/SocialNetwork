from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.

class Post(models.Model):
	text = models.CharField(max_length = 160)
	post_time = models.DateTimeField(default=datetime.now, blank=True)
	user = models.ForeignKey(User)
	def __unicode__(self):
		return self.text
	
		
class Entry(models.Model):
	first_name = models.CharField(max_length = 100, blank = True)
	last_name = models.CharField(max_length = 100, blank = True)
	age = models.DecimalField(max_digits = 3, decimal_places = 0, blank = True)
	photo = models.ImageField(upload_to = "person-photo", blank = True)
	bio = models.CharField(max_length = 430, blank = True)
	user = models.OneToOneField(
		User,
		on_delete = models.CASCADE,
		primary_key = True,
	)
	def __unicode__(self):
		return self.first_name + " " + self.last_name

class Follow(models.Model):
	user = models.ForeignKey(User)
	follow_posts = models.ManyToManyField(Post)
	def __unicode__(self):
		return "follow"
		
class Comment(models.Model):
	post = models.ForeignKey(Post)
	comment_person = models.CharField(max_length = 100)
	comment_time = models.DateTimeField(default = datetime.now)
	text = models.CharField(max_length = 430, blank = True)
	def __unicode__(self):
		return self.comment_text