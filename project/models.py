from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Project(models.Model):
	NO_CATEGORY = 0
	TEXT_RECOGNITION = 1
	IMAGE_RECOGNITION = 2
	NUMBERS_RECOGNITION = 3
	CATEGORIES  = (
		(NO_CATEGORY, 'NC - No Category'),
		(TEXT_RECOGNITION, 'T - Text Recognition'),
		(IMAGE_RECOGNITION, 'I - Image Recognition'),
		(NUMBERS_RECOGNITION, 'N - Numbers Recognition'),
		)
	author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
	title = models.CharField(max_length=200)
	description = models.TextField()
	created = models.DateTimeField(default=timezone.now)
	category = models.IntegerField(choices=CATEGORIES, default=NO_CATEGORY)
	website = models.URLField(blank=True)

	class Meta:
		ordering = ('-created', 'title')

	def get_absolute_url(self):
		return reverse("project_detail",kwargs={'pk':self.pk})

	def __str__(self):
		return self.title


class Label(models.Model):
	project = models.ForeignKey(to='Project', related_name='labels', on_delete=models.CASCADE )
	text = models.CharField(max_length=200)
	created = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.text

	def get_absolute_url(self):
		return reverse("project_list")



class Doc(models.Model):
	label = models.ForeignKey(to='Label', related_name='docs', on_delete=models.CASCADE )
	text = models.TextField()

	def get_absolute_url(self):
		return reverse("project_list")


	def __str__(self):
		return self.text