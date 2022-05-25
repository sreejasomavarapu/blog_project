from re import template
from ssl import HAS_TLSv1_1
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Post
from django.views.generic import ListView, DetailView,CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.models import User
 

# posts=[
#     {
#         'author':'Sreeja',
#         'title': 'Blog Post 1',
#         'content':'First Post content',
#         'date_posted':'April 2,2022'
#     },
#     {
#         'author':'Sreeja S',
#         'title': 'Blog Post 2',
#         'content':'Second Post content',
#         'date_posted':'April 3,2022'


#     }
# ]





def home(request):
    # return HttpResponse('<h1>Home page</h1>')
    context={'posts':Post.objects.all()}
    return render(request,'blog/home.html',context)

class PostListView(ListView):
    model=Post
    template_name='blog/home.html'
    context_object_name='posts'
    ordering=['-date_posted']
    paginate_by=5

class UserPostListView(ListView):
    model=Post
    template_name='blog/user_posts.html'
    context_object_name='posts'
    paginate_by=5

    def get_queryset(self):
        user=get_object_or_404(User ,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')



class PostDetailView(DetailView):
    model=Post



class PostCreateView(LoginRequiredMixin ,CreateView):
    model=Post
    fields=['title','content']

    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)
    
class PostUpdateView( UserPassesTestMixin ,LoginRequiredMixin ,UpdateView):
    model=Post
    fields=['title','content']

    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)
    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
            return True
        return False
class PostDeleteView(UserPassesTestMixin ,LoginRequiredMixin ,DeleteView):
    model=Post
    success_url='/'
    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
            return True
        return False
    
    

def about(request):
    return render(request,'blog/about.html')

