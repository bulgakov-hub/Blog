from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
	"""Пост пользователя"""

	author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
	title = models.CharField('Заголовок', max_length=150)
	content = models.TextField('Текст', max_length=10000)
	date = models.DateTimeField('Дата публикации', auto_now_add=True)
	users_read = models.ManyToManyField(User, related_name='post_read', blank=True, verbose_name='Пост читали')

	def get_absolute_url(self):
		return reverse('posts:detail', kwargs={'pk': self.pk})
	
	def __str__(self):
		return self.title

	class Meta:
		ordering = ['-date']
		verbose_name = ('Пост пользователя')
		verbose_name_plural = ('Посты пользователей')
