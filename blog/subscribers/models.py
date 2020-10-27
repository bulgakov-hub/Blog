from django.db import models
from django.contrib.auth.models import User
from posts.models import Post
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from django.core.mail import send_mass_mail
from django.conf import settings
from django.urls import reverse


class Subscribers(models.Model):
	"""Подписчики пользователя"""

	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
	subscriber = models.ForeignKey(User, on_delete=models.CASCADE, related_name='signer')
	date = models.DateTimeField('Дата подписки', auto_now_add=True)

	class Meta:
		ordering = ['-date']

	def __str__(self):
		return '{} подписан {}'.format(self.user, self.subscriber)


# Перед удалением подписки удаляем наши отметки о прочтенных постах
@receiver(pre_delete, sender=Subscribers)
def pre_delete_story(sender, instance, **kwargs):

	author = instance.user
	user = instance.subscriber
	
	find_post = Post.objects.filter(author=author).filter(users_read__id=user.id)
	for post in find_post:
		post.users_read.remove(user)


# Сигнал отправка почты подписчикам после создания поста
@receiver(signal=post_save, sender=Post)
def send_message(sender, instance, **kwargs):
	author = instance.author
	subscribers_list = Subscribers.objects.filter(user=author)
	recipient_list = [user.subscriber.email for user in subscribers_list if user.subscriber.email]
	print(recipient_list)
	print([user for user in instance.users_read.all()])
	subject = 'Новый пост от автора {}'.format(instance.author)
	message = 'Новый пост доступен по ссылке: {}'.format(instance.get_absolute_url())
	from_email = settings.DEFAULT_FROM_EMAIL
	
	messages = ()
	for email in recipient_list:  
		messages = messages + ((subject, message, from_email, [email]),)

	send_mass_mail(messages, fail_silently=False)