from django.db import models

# Create your models here.

class User(models.Model):
	first_name=models.CharField(max_length=40)
	last_name=models.CharField(max_length=40)
	email=models.CharField(max_length=40)
	password=models.CharField(max_length=100)
	verification_string=models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)