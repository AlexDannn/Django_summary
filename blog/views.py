from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from .models import Post, Comments
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from .forms import CommentsForm
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.db.models import Value, IntegerField


'''
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 3
'''

def post_list_view(request):
    posts = Post.objects.all().order_by('-date_posted')
    comments = Comments.objects.all()
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/home.html', {'posts': posts, 'comments': comments, 'page_obj': page_obj})

'''
class PostDetailView(DetailView):
    model = Post
    post = self.get_object()
    comments = Post.objects.filter(post=post)
'''

def post_detail_view(request, pk):
    post = get_object_or_404(Post, id=pk)
    comments = Comments.objects.filter(post=post).order_by('-id')

    if request.method == 'POST':
        comment_form = CommentsForm(request.POST or None)
        if comment_form.is_valid():
            body = request.POST.get('body')
            comment = Comments.objects.create(post=post, user=request.user, body=body)
            comment.save()
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        comment_form = CommentsForm()

    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


def about(request):
    return render(request, 'blog/about.html', {'titke': 'about'})


'''
class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5
    
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
'''
