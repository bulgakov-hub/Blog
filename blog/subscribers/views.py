from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import ListView, View, TemplateView
from django.views.generic.edit import DeleteView
from .models import Subscribers
from django.contrib.auth.mixins import LoginRequiredMixin
from posts.models import Post


class SubscribersListView(LoginRequiredMixin, ListView):
    """Мои подписки на пользователей"""

    model = Subscribers
    template_name = 'subscribers/list.html'
    context_object_name = 'subscribers'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(subscriber=self.request.user)

    def get_context_data(self):
        context = super().get_context_data()
        users_object = [f.user.id for f in self.object_list]
        context['user_blogs'] = User.objects.all().exclude(
            id=self.request.user.id).exclude(id__in=users_object).values_list(
            'id', 'username', named=True)

        return context


class SubscribersCreateView(LoginRequiredMixin, View):
    """Подписаться на блог"""

    def post(self, request, pk):
        user = get_object_or_404(User, id=pk)
        Subscribers.objects.create(subscriber=request.user, user=user)

        return redirect('subscribers:list')


class SubscribersDeleteView(LoginRequiredMixin, DeleteView):
    """Удалить подписку"""

    model = Subscribers
    template_name = 'subscribers/delete.html'
    success_url = reverse_lazy('subscribers:list')

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(subscriber=self.request.user)


class NewsFeedView(LoginRequiredMixin, TemplateView):
    """Новостная лента"""

    template_name = 'subscribers/news_feed.html'

    def get_context_data(self):
        context = super().get_context_data()
        post = Post.objects.exclude(author=self.request.user)
        subscriber_ids = self.request.user.signer.values_list(
            'user_id', flat=True)
        if subscriber_ids:
            post = post.filter(author_id__in=subscriber_ids)
        post = post[:20]
        context['news_feed'] = post

        return context
