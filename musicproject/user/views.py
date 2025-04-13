from django.shortcuts import render, redirect
from user.models import *
from django.db.models import Q
from django.contrib.auth import logout, login
from django.contrib.auth.hashers import check_password
from .form import MyUserCreationForm
from index.models import *

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.decorators import login_required

# Create your views here.

def loginview(request):
    # 表单对象
    user = MyUserCreationForm()
    tips = None

    # 表单提交
    if request.method == 'POST':
        # 判断表单提交时用户登录还是用户注册
        if request.POST.get('loginUser', ''):
            # 用户登录
            loginUser = request.POST.get('loginUser', '')
            password = request.POST.get('password', '')
            user_qs = MyUser.objects.filter(Q(mobile=loginUser) | Q(username=loginUser))
            if user_qs.exists():
                user = user_qs.first()
                if check_password(password, user.password):
                    login(request, user)
                    return redirect('/user/home/1.html')
                else:
                    tips = '密码错误'
            else:
                tips = '用户不存在'
        else:
            # 用户注册
            user = MyUserCreationForm(request.POST)
            if user.is_valid():
                user.save()
                tips = '注册成功'
            else:
                # 输出所有错误信息以进行调试
                errors = user.errors.as_data()
                if user.errors.get('username'):
                    tips = user.errors.get('username', ['注册失败'])[0]
                elif user.errors.get('mobile'):
                    tips = user.errors.get('mobile', ['注册失败'])[0]
                else:
                    tips = '注册失败'
                print(f"注册错误: {errors}")

    return render(request, 'login.html', {'user': user, 'tips': tips})


def logoutview(request):
    logout(request)
    return redirect('/')


# 个人中心
@login_required(login_url='/user/login.html')
def homeview(request, page):
    # 热搜歌曲
    search_song = Dynamic.objects.select_related('song').order_by('-dynamic_search').all()[:6]
    # 分页功能
    song_info = request.session.get('play_list', [])
    print(song_info)
    paginator = Paginator(song_info, 3)
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'home.html', locals())
