from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Contest, Post
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class PostCreate(CreateView):
    model = Post
    fields = '__all__'
    success_url = '/'

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
    success_url = '/'

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
    return render(request, 'landing.html', {'contests': contests })

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
