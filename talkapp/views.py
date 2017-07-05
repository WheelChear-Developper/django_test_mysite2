from django.shortcuts import render, redirect
from talkapp.models import PostMessage, Profile
from django.contrib.auth.models import User
from django.conf import settings
from django.conf.urls.static import static
#ユーザー認証
from django.contrib.auth import authenticate, login

from datetime import datetime

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

    #システム時間取得
    now = datetime.now().strftime("%Y%m%d-%H%M%S")
    print("\033[94m", "system time = ", now, "\033[0m")

    #ファイル名取得（未設定ではエラー）
    image_file = request.FILES['file']
    print("\033[94m", "image_file = ", image_file, "\033[0m")

    #パス設定
    path = UPLOAD_DIR + str(now) + image_file.name
    print("\033[94m", "path = ", path, "\033[0m")

    #ファイル書き込み
    destination = open(path, 'wb+')
    for chunk in image_file.chunks():
        destination.write(chunk)
    destination.close()

    #プロファイルデータ保存（ユーザー番号に紐づく画像ファイル設定）
    profile = Profile()
    profile.image = str(now) + image_file.name
    profile.user = user
    profile.save()

    check_user = authenticate(username=username, password=password)
    if check_user is not None:
        if check_user.is_active:
            login(request, check_user)

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
