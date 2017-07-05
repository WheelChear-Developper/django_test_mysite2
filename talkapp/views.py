from django.shortcuts import render, redirect
from talkapp.models import PostMessage, Profile
from django.contrib.auth.models import User

from django.conf import settings
from django.conf.urls.static import static


UPLOAD_DIR = settings.MEDIA_ROOT + "/images/"

def home(request):
    return render(request, 'talkapp/home.html')

def user_create(request):
    return render(request, 'talkapp/user_create.html')

def user_store(request):
    username = request.POST["name"]
    email = request.POST["email"]
    password = request.POST["password"]

    #入力したユーザー情報
    print("\033[94m", "username = ", username, "\033[0m")
    print("\033[94m", "email = ", email, "\033[0m")
    print("\033[94m", "password = ", password, "\033[0m")

    #ユーザー情報登録
    user = User.objects.create_user(username, email, password)
    user.save()

    print("\033[94m", "UPLOAD_DIR = ", UPLOAD_DIR, "\033[0m")

    now = time.time()
#    image_file = request.FILES['file']
#    path = UPLOAD_DIR + str(now) + image_file.name
#    destination = open(path, 'wb+')
#    for chunck in image_file.chunk():
#        destination.write(chunck)
#    destination.close()

#    profile = profile()
#    profile.image = str(now) + image_file.name
#    profile.user = user
#    profile.save()

#    user = authenticate(username=username, password=password)
#    if user is not None:
#        if user.is_active:
#            login(request, user)

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
    return redirect('talkapp:post_index')


def getlogin(request):
    return render(request, 'talkapp/getlogin.html')

def postlogin(request):
    return redirect('talkapp:post_index')

def getlogout(request):
    return render(request, 'talkapp/home.html')
