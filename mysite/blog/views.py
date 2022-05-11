from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.views.generic.edit import FormMixin
from .forms import ArticleCommentForm
from django.shortcuts import render, get_object_or_404

from .models import Article, ArticleComment
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView)


class ArticlesListView(ListView):
    model = Article
    context_object_name = 'articles'
    template_name = 'articles.html'
    paginate_by = 3

    def get_queryset(self):
        articles = list(reversed(Article.objects.all()))
        return articles


class ArticleDetailView(DetailView, FormMixin):
    model = Article
    template_name = 'article_detail.html'
    form_class = ArticleCommentForm

    def get_success_url(self):
        return reverse('article_detail', kwargs={'pk': self.object.id})

    def get_context_data(self, *args, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(*args, **kwargs)
        context['form'] = ArticleCommentForm(initial={'article': self.object})
        context['comments'] = list(reversed(ArticleComment.objects.filter(article=self.object)))
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.article = self.object
        form.instance.reviewer = self.request.user
        form.save()
        return super(ArticleDetailView, self).form_valid(form)


class MyArticlesListView(LoginRequiredMixin, ListView):
    model = Article
    context_object_name = 'articles'
    template_name = 'my_articles.html'
    paginate_by = 3

    def get_queryset(self):
        articles = list(reversed(Article.objects.filter(user=self.request.user)))
        return articles


class MyArticleDetailView(DetailView):
    model = Article
    template_name = 'my_article_detail.html'


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = 'article_add.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('articles')


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    fields = ['title', 'content']
    template_name = 'article_update.html'

    def get_success_url(self):
        return reverse('my_articles_detail', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        article = self.get_object()
        return self.request.user == article.user


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    success_url = "/my_articles/"
    template_name = 'article_delete.html'

    def test_func(self):
        article = self.get_object()
        return self.request.user == article.user


class ArticleCommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ArticleComment
    form_class = ArticleCommentForm
    template_name = 'comments_update.html'

    def get_success_url(self):
        return reverse('articles')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        articleComment = self.get_object()
        return self.request.user == articleComment.reviewer


class ArticleCommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ArticleComment
    success_url = "/articles/"
    template_name = 'comments_delete.html'

    def test_func(self):
        articleComment = self.get_object()
        return self.request.user == articleComment.reviewer



@csrf_protect
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        if username == "" or email == "":
            messages.error(request, f" You left empty fields!")
            return redirect('register')
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, f" User's name {username} have been taken already!")
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'User with email {email} have been taken already!')
                    return redirect('register')
                else:
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.success(request, f'New user have been created, you can log in.')
                    return redirect('register')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('register')
    return render(request, 'registration/register.html')