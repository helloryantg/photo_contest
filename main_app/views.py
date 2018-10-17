from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LoginForm, CommentForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Contest, Post, Comment, Like
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import uuid
import boto3

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'like-photo-contest'

class CommentUpdate(UpdateView):
    model = Comment
    fields = ['text']
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return redirect(f"/posts/{self.object.post_id}")

@method_decorator(login_required, name='dispatch')
class CommentDelete(DeleteView):
    model = Comment
    def post(self, request, *args, **kwargs):
        post_id = self.get_object().post_id
        Comment.objects.get(id=int(kwargs['pk'])).delete()
        return redirect(f"/posts/{post_id}")

class PostCreate(CreateView):
    model = Post
    fields = ['title', 'description', 'category']

    def form_valid(self, form):
       post = form.instance
       post.user = self.request.user
       post.contest_id = int(self.kwargs['contest_id'])
       photo_file = self.request.FILES.get('photo-file', None)
       if photo_file:
           s3 = boto3.client('s3')
           key = uuid.uuid4().hex[:6] + \
               photo_file.name[photo_file.name.rfind('.'):]
           try:
               s3.upload_fileobj(photo_file, BUCKET, key)
               photo_url = f"{S3_BASE_URL}{BUCKET}/{key}"
               post.photo_url = photo_url
           except:
               print('An error occurred uploading file to S3')
       post.save()
       return redirect("/")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contest_id'] = int(self.kwargs['contest_id'])
        return context

class PostUpdate(UpdateView):
    model = Post
    fields = '__all__'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return HttpResponseRedirect('/')

@method_decorator(login_required, name='dispatch')
class PostDelete(DeleteView):
    model = Post

    def post(self, request, *args, **kwargs):
       self.object = self.get_object()
       if self.object.user == request.user:
           self.object.delete()
           return redirect('/')
       else:
           return redirect('/')

class ContestCreate(CreateView):
    model = Contest
    fields = '__all__'
    success_url = '/'

class ContestUpdate(UpdateView):
    model = Contest
    fields = '__all__'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return HttpResponseRedirect('/')

@method_decorator(login_required, name='dispatch')
class ContestDelete(DeleteView):
    model = Contest
    success_url = '/'

# Create your views here.
def landing(request):
    contests = Contest.objects.all()
    return render(request, 'landing.html', { 'contests': contests })

def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username = u, password = p)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    print("The account has been disabled.")
                    return HttpResponseRedirect('/')
            else:
                print("The username and/or password is incorrect.")
                return HttpResponseRedirect('/')
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})

@login_required
def my_account(request, id):
    account = User.objects.get(id=id)
    posts = request.user.post_set.all()
    return render(request, 'my_account.html', { 'account': account, 'posts': posts })

def photos_page(request, contest_id):
    contest = Contest.objects.get(id=contest_id)
    cat = request.GET.get('category', 'N')
    posts = contest.post_set.filter(category=cat)
    return render(request, 'contests/index.html', {'contest': contest, 'posts' : posts, 'cat': cat})

def posts_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    has_liked_category = Like.objects.filter(post__category=post.category, user=request.user).exists()
    has_liked = Like.objects.filter(post=post, user=request.user).exists()
    comments = Comment.objects.filter(post=post)
    likes = post.like_set.all().count()
    comment_form = CommentForm()
    return render(request, 'posts/detail.html', { 'post': post, 'comment_form' : comment_form, 'comments': comments, 'likes': likes, 'has_liked_category': has_liked_category, 'has_liked': has_liked })

@login_required
def add_comment(request, post_id):
    form = CommentForm(request.POST)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.post_id = post_id
        new_comment.user = request.user
        new_comment.save()
    return redirect('posts_detail', post_id=post_id)

def add_like(request, post_id):
    post = Post.objects.get(id=post_id)
    has_liked = Like.objects.filter(post__category=post.category, user=request.user).exists()
    if not has_liked:
        new_like, created = Like.objects.get_or_create(user=request.user, post_id=post_id)
    return redirect('posts_detail', post_id=post_id)

  


