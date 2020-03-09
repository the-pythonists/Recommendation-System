from django.db import models

# Create your models here.

class Videos_Data(models.Model):
	Video_Id = models.CharField(max_length=30,default='')
	Title = models.CharField(max_length=100)
	Channel_Name = models.CharField(max_length=100)
	Category = models.CharField(max_length=50)
	Description = models.CharField(max_length=1000)
	Views = models.IntegerField(default=0)
	Likes = models.IntegerField(default=0)
	Dislikes = models.IntegerField(default=0)
	Comments = models.CharField(max_length=1000)
	Date = models.CharField(max_length=10)
	Time = models.CharField(max_length=10)
	Thumb = models.ImageField(upload_to='media')
	Video = models.FileField(upload_to='media')

	def __str__(self):
		return self.Title

class Users(models.Model):
	UserId = models.CharField(max_length=30)
	Name = models.CharField(max_length=100)
	Channel_Name = models.CharField(max_length=50)
	Email = models.CharField(max_length=50)
	Password = models.CharField(max_length=100)
	Date = models.CharField(max_length=10)
	Time = models.CharField(max_length=10)
	Image = models.ImageField(upload_to='media',default='media/profile.jpeg')
	# upload_to='images',default='images/demo.jpg'

	def __str__(self):
		return self.Name

class Subscription(models.Model):
	email=models.CharField(max_length=100)

	def __str__(self):
		return self.email