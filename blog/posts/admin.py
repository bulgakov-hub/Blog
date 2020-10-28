from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
	"""Посты в админке"""

	model = Post
	list_display = ('author', 'title', 'date')


admin.site.register(Post, PostAdmin)