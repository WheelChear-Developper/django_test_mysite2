from django.shortcuts import render, redirect
from talkapp.models import PostMessage
#from django.contrib.auth.models import User

def home(request):
    return render(request, 'talkapp/home.html')

def user_create(request):
    return render(request, 'talkapp/user_create.html')

def user_store(request):
    username = request.POST["name"]
    email = request.POST["email"]
    password = request.POST["password"]

    print("username:", username)

#    user = User.objects.create_user(username, email, password)
#    user.save()

    return redirect('talkapp:post_index')

def user_edit(request):
    return render(request, 'talkapp/user_edit.html')

def user_update(request):
    return redirect('talkapp:post_index')

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
    post = PostMessage()
    post.message = request.POST["message"]

    #ログインしていないと、NULLとなる(ADMINログイン)
    print("\033[94m", "User = ", request.user, "\033[0m")
    post.user = request.user

    post.save()

    return redirect('talkapp:post_index')


def post_delete_all(request):
    PostMessage.objects.all().delete()
#    return redirect('post_index')


def getlogin(request):
    return render(request, 'talkapp/getlogin.html')

def postlogin(request):
    return redirect('talkapp:post_index')

def getlogout(request):
    return render(request, 'talkapp/home.html')
