from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post


class PostListView(LoginRequiredMixin, ListView):
	"""Просмотр постов пользователей"""

	model = Post
	template_name = 'posts/list.html'
	context_object_name = 'posts'
	paginate_by = 10

	def get_queryset(self):
		qs = super().get_queryset()
		return qs.filter(author=self.request.user)


class PostCreateView(LoginRequiredMixin, CreateView):
	"""Создание поста пользователя"""

	model = Post
	template_name = 'posts/modify.html'
	fields = ['title', 'content']
	success_url = reverse_lazy('posts:list')

	def get_context_data(self):
		context = super().get_context_data()
		context['name'] = 'Создать пост'
		return context

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
	"""Изменить пост пользователя"""

	model = Post
	template_name = 'posts/modify.html'
	fields = ['title', 'content']
	success_url = reverse_lazy('posts:list')

	def get_context_data(self):
		context = super().get_context_data()
		context['name'] = 'Изменить пост'
		return context


class PostDeleteView(LoginRequiredMixin, DeleteView):
	"""Удалить пост пользователя"""

	model = Post
	template_name = 'posts/delete.html'
	success_url = reverse_lazy('posts:list')

	def get_queryset(self):
		qs = super().get_queryset()
		return qs.filter(author=self.request.user)


class PostDetailView(DetailView):
	"""Просмотр поста пользователя"""

	model = Post
	template_name = 'posts/detail.html'


class ReadPostView(LoginRequiredMixin, View):
	"""Отметка о прочтении поста"""

	def post(self, request, pk):
		post = get_object_or_404(Post, id=pk)
		users_read_ids = post.users_read.values_list('id', flat=True)

		if request.user.id in users_read_ids:
			post.users_read.remove(request.user)
		else:
			post.users_read.add(request.user)

		return redirect('posts:detail', pk=pk)
