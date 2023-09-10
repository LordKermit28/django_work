from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy, reverse
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView
from blog.forms import BlogForm
from blog.models import Blog


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blog:list_blog')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        return context_data

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save(commit=False)
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()
            return super().form_valid(form)
        else:
            return self.form_valid(form)

class BlogListView(ListView):
    model = Blog
    template_name = 'blog/blog_list.html'
    context_object_name = 'blogs'

class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blog:list_blog')


class BlogDetailView(LoginRequiredMixin, DetailView):
    model = Blog


    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.view_count is None:
            self.object.view_count = 0
        self.object.view_count += 1
        self.object.save()
        return self.object


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:list_blog')

