from django.shortcuts import render, redirect
#アカウント情報取得用
from django.contrib.auth.models import User
#プロジェクト設定取得用
from django.conf import settings
#ユーザー認証
from django.contrib.auth import authenticate, login, logout

#モデル取得用
from talkapp.models import PostMessage, Profile

#エラー時の処理用
from . import forms
#サーバーの画像ファイル削除必要用
import os

from datetime import datetime

UPLOAD_DIR = os.path.join(settings.BASE_DIR, 'talkapp') + "/static/images/"

def home(request):
    return render(request, 'talkapp/home.html')

def user_create(request):
    return render(request, 'talkapp/user_create.html')

def user_store(request):

    # 入力値取得
    username = request.POST["name"]
    email = request.POST["email"]
    password = request.POST["password"]

    # 画像ファイルセット
    if 'file' in request.FILES:
        image_file = request.FILES['file']
    else:
        image_file = ''

    # 入力したユーザー情報
    print("\033[94m", "username = ", username, "\033[0m")
    print("\033[94m", "email = ", email, "\033[0m")
    print("\033[94m", "password = ", password, "\033[0m")
    print("\033[94m", "image_file = ", image_file, "\033[0m")
    print("\033[94m", "UPLOAD_DIR = ", UPLOAD_DIR, "\033[0m")

    # 名前入力チェック
    if username == '':
        form = forms.UserCreateForm(request.GET or None)
        contdir = {
            'form': form,
            'message_title': 'エラー：',
            'message': '名前が入力されていません',
            'username': username,
            'email': email,
            'password': password,
        }
        return render(request, 'talkapp/user_create.html', contdir)

    # メールアドレス入力チェック
    if email == '':
        form = forms.UserCreateForm(request.GET or None)
        contdir = {
            'form': form,
            'message_title': 'エラー：',
            'message': 'メールアドレスが入力されていません',
            'username': username,
            'email': email,
            'password': password,
        }
        return render(request, 'talkapp/user_create.html', contdir)

    # パスワード入力チェック
    if password == '':
        form = forms.UserCreateForm(request.GET or None)
        contdir = {
            'form': form,
            'message_title': 'エラー：',
            'message': 'パスワードが入力されていません',
            'username': username,
            'email': email,
            'password': password,
        }
        return render(request, 'talkapp/user_create.html', contdir)

    # ユーザー情報登録
    user = User.objects.create_user(username, email, password)
    user.save()

    # システム時間取得
    now = datetime.now().strftime("%Y%m%d-%H%M%S")
    print("\033[94m", "system time = ", now, "\033[0m")

    # パス設定(無い場合は、初期画像セット)
    if image_file == '':
        path = UPLOAD_DIR + 'no_image.png'

        # プロファイルデータ保存（ユーザー番号に紐づく画像ファイル設定）
        profile = Profile()
        profile.image = 'no_image.png'
        profile.user = user
        profile.save()

    else:
        path = UPLOAD_DIR + str(now) + image_file.name

        # ファイル書き込み
        destination = open(path, 'wb+')
        for chunk in image_file.chunks():
            destination.write(chunk)
        destination.close()

        # プロファイルデータ保存（ユーザー番号に紐づく画像ファイル設定）
        profile = Profile()
        profile.image = str(now) + image_file.name
        profile.user = user
        profile.save()
    print("\033[94m", "Save Image PathFile = ", path, "\033[0m")

    # ログイン処理
    check_user = authenticate(username=username, password=password)
    if check_user is not None:
        if check_user.is_active:
            login(request, check_user)

    return redirect('talkapp:post_index')

def user_edit(request):

    user = request.user
    context = {
        'user' : user,
        'username': user.username,
        'email': user.email,
        'user_image': user.profile.image,
    }
    return render(request, 'talkapp/user_edit.html' , context)

def user_update(request):

    # ログインユーザー情報取得
    user = request.user

    # 名前が渡されてくれた場合、名前変更
    if request.POST["name"] != '':
        user.username = request.POST["name"]
    # メールアドレスが渡されてくれた場合、メールアドレス変更
    if request.POST["email"] != '':
        user.email = request.POST["email"]
    # パスワードが渡されてくれた場合、パスワード変更
#    if request.POST["password"] != '':
#        user.set_password(request.POST["password"])

    # 現在パスワード入力チェック
    if request.POST["check_password"] == '':
        form = forms.UserEditForm(request.GET or None)
        contdir = {
            'form': form,
            'message_title': 'エラー：',
            'message': '現在のパスワードが入力されていません。',
            'username': user.username,
            'email': user.email,
        }
        return render(request, 'talkapp/user_edit.html', contdir)

    # パスワード入力チェック(現在のメールと同じであるか)
    if user.check_password(request.POST["check_password"]) == False:
        form = forms.UserEditForm(request.GET or None)
        contdir = {
            'form': form,
            'message_title': 'エラー：',
            'message': '現在のパスワードが間違っています。',
            'username': user.username,
            'email': user.email,
        }
        return render(request, 'talkapp/user_edit.html', contdir)

    # パスワード入力チェック
    if request.POST["password"] == '':
        form = forms.UserEditForm(request.GET or None)
        contdir = {
            'form': form,
            'message_title': 'エラー：',
            'message': '新しいパスワードが入力されていません。',
            'username': user.username,
            'email': user.email,
        }
        return render(request, 'talkapp/user_edit.html', contdir)
    # パスワード更新
    user.set_password(request.POST["password"])

    # ユーザー情報保存
    user.save()

    # プロファイル画像更新
    if 'file' in request.FILES:

        # 画像ファイル指定での更新
        # 削除ファイル
        print("\033[94m", "delete_image_file = ", user.profile.image, "\033[0m")
        # 更新前のプロファイル画像を削除
        old_image_file = UPLOAD_DIR + user.profile.image

        if user.profile.image != 'no_image.png':
            os.remove(old_image_file)

        # システム時間取得
        now = datetime.now().strftime("%Y%m%d-%H%M%S")
        print("\033[94m", "system time = ", now, "\033[0m")

        # ファイル名取得（未設定ではエラー）
        image_file = request.FILES['file']
        print("\033[94m", "image_file = ", image_file, "\033[0m")

        # パス設定
        path = UPLOAD_DIR + str(now) + image_file.name
        print("\033[94m", "path = ", path, "\033[0m")

        # ファイル書き込み
        destination = open(path, 'wb+')
        for chunk in image_file.chunks():
            destination.write(chunk)
        destination.close()

        # プロファイルデータ保存（ユーザー番号に紐づく画像ファイル設定）
        user.profile.image = str(now) + image_file.name
        user.profile.save()
    else:

        # 画像ファイルの初期値設定
        # ファイル名取得（未設定ではエラー）
        image_file = 'no_image.png'
        print("\033[94m", "image_file = ", image_file, "\033[0m")

        # プロファイルデータ保存（ユーザー番号に紐づく画像ファイル設定）
        user.profile.image = image_file
        user.profile.save()

    #ログイン処理
    if request.POST["password"] != '':
        user = authenticate(username=user, password=request.POST["password"])
        if user is not None:
            if user.is_active:
                login(request, user)

    return redirect('talkapp:post_index')

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
    email = request.POST["email"]
    password = request.POST["password"]

    try:
        username = User.objects.get(email=email).username
    except User.DoesNotExist:
        username = None

    if username is not None:
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('talkapp:post_index')

    return render(request, 'talkapp/getlogin.html')

def getlogout(request):
    logout(request)
    return render(request, 'talkapp/home.html')
