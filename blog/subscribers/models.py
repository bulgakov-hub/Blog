from django.db import models
from django.contrib.auth.models import User


class Subscribers(models.Model):
	"""Подписчики пользователя"""

	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
	subscriber = models.ForeignKey(User, on_delete=models.CASCADE, related_name='signer')
	date = models.DateTimeField('Дата подписки', auto_now_add=True)

	class Meta:
		ordering = ['-date']

	def __str__(self):
		return '{} подписан {}'.format(self.user, self.subscriber)