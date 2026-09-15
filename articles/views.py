from django.shortcuts import get_object_or_404, redirect, render
from .models import Category,Blog, About
from django.db.models import Q
from .forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth

def home(request):
    featured_post = Blog.objects.filter(
        is_featured=True,
        status='Published'
    ).order_by('updated_at')

    posts = Blog.objects.filter(
        is_featured=False,
        status='Published'
    )
    try:
        about = About.objects.all()
    except:
        about = None

    context = {
        "featured_post": featured_post,
        "posts": posts,
        'about':about,
    }

    return render(request, "home.html", context)



def post_by_category(request, category_id):

    category = get_object_or_404(
        Category,
        pk=category_id
    )

    posts = Blog.objects.filter(
        status="Published",
        category=category
    ).order_by('-created_at')

    context = {
        "posts": posts,
        "category": category,
    }

    return render(
        request,
        "post_by_category.html",
        context
    )


def blogs(request, slug):
    single_blog = get_object_or_404(
        Blog,
        slug=slug,
        status='Published'
    )

    context = {
        "single_blog": single_blog,
    }

    return render(
        request,
        "blogs.html",
        context
    )


def search(request):
    keyword = request.GET.get('keyword', '')

    blogs = Blog.objects.filter(
        Q(title__icontains=keyword) |
        Q(short_description__icontains=keyword) |
        Q(blog_body__icontains=keyword),
        status='Published'
    )

    context = {
        'blogs': blogs,
        "keyword":keyword
    }

    return render(request, 'search.html', context)

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            print(form.errors)
    else:
        form = RegistrationForm()   

    context = {
        'form':form }
    
    return render(request, 'register.html', context)

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request,request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username,password=password)
            if user is not None:
                auth.login(request,user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    context = {
        "form":form
    }
    return render(request, 'login.html',context=context)

def logout(request):
    auth.logout(request)
    return redirect('home')