from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
	"""Пост пользователя"""

	author = models.ForeignKey(User, on_delete=models.CASCADE)
	title = models.CharField('Заголовок', max_length=150)
	content = models.TextField('Текст', max_length=10000)
	date = models.DateTimeField('Дата публикации', auto_now_add=True)

	def __str__(self):
		return self.title

	class Meta:
		ordering = ['-date']
		verbose_name = ('Пост пользователя')
		verbose_name = ('Посты пользователей')
