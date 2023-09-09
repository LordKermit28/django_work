from django.urls import path
from django.views.decorators.cache import cache_page

from blog.views import BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView

app_name = 'blog'

urlpatterns = [
    path('list_blog', BlogListView.as_view(), name='list_blog'),
    path('view_blog/<int:pk>/', BlogDetailView.as_view(), name='view_blog'),
    path('create_blog/', BlogCreateView.as_view(), name='create_blog'),
    path('edit/<int:pk>/', BlogUpdateView.as_view(), name='edit_blog'),
    path('delete_blog/<int:pk>/', BlogDeleteView.as_view(), name='delete_blog'),]