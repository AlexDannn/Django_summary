from django.urls import path
from .views import   PostCreateView, PostDeleteView
from . import views

urlpatterns = [
    #path('', PostListView.as_view(), name='blog-home'),
    #path('post/<int:pk>', PostDetailView.as_view(), name='post-detail'),
    path('', views.post_list_view, name='blog-home'),
    path('post/<int:pk>/', views.post_detail_view, name='post-detail'),
    #path('post/<int:pk>/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    ]