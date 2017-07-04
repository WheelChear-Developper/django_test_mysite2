from django.shortcuts import render, redirect
from talkapp.models import PostMessage

def home(request):
    return render(request, 'talkapp/home.html')

def user_create(request):
    return render(request, 'talkapp/user_create.html')

def user_store(request):
    return redirect('post_index')

def user_edit(request):
    return render(request, 'talkapp/user_edit.html')

def user_update(request):
    return redirect('post_index')

class Post:
    def __init__(self):
        self.message = ""

def post_index(request):
    posts = PostMessage.objects.all()
    context = {
        'posts' : posts
    }
    return render(request, 'talkapp/post_index.html', context)

def post_create(request):
    return render(request, 'talkapp/post_create.html')

def post_store(request):
    posts = PostMessage()
    post.message = request.POST('message')
    post.user = request.user
    post.save()

    return redirect('post_index')


def post_delete_all(request):
    PostMessage.objects.all().delete()
#    return redirect('post_index')


def getlogin(request):
    return render(request, 'talkapp/getlogin.html')

def postlogin(request):
    return redirect('post_index')

def getlogout(request):
    return render(request, 'talkapp/home.html')
