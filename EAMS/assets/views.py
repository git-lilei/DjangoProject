from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
# Create your views here.
from django.shortcuts import get_object_or_404
from .models import *


# 首页
def index(request):
    if request.session.get('username'):
        # user = User.objects.get(name=request.session.get('username'))
        # assets = Asset.objects.filter(admin=user)

        assets = User.objects.get(name=request.session.get('username')).user.all()

        # admin1 = User.objects.get(name='test1')
        # print(admin1,type(admin1))
        # print(admin1.asset_set)
        # assets = admin1.asset_set.all()

        return render(request, 'assets/index.html', locals())
    else:
        assets = Asset.objects.all()
        return render(request, 'assets/index.html', locals())


# 详情页
def detail(request, asset_id):
    asset = get_object_or_404(Asset, pk=asset_id)
    return render(request, 'assets/detail.html', locals())


# 用户登录
def login(request):
    if request.method == 'GET':
        return render(request, 'assets/login.html')
    elif request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        message = '所有字段斗必须填写'
        if username and password:
            username = username.strip()
            try:
                user = User.objects.get(name=username)
                if user.password == password:
                    request.session['username'] = user.name
                    return redirect(reverse('assets:index'))
                else:
                    message = '密码不正确！'
            except:
                message = '用户不存在！'
        return render(request, 'assets/login.html', {'message': message})


# 退出登录
def logout(request):
    del request.session['username']
    return redirect(reverse('assets:login'))


# 设备概况
def dashboard(request):
    total = Asset.objects.count()
    upline = Asset.objects.filter(status=0).count()
    offline = Asset.objects.filter(status=1).count()
    unknown = Asset.objects.filter(status=2).count()
    breakdown = Asset.objects.filter(status=3).count()
    backup = Asset.objects.filter(status=4).count()

    up_rate = round(upline / total * 100)
    o_rate = round(offline / total * 100)
    un_rate = round(unknown / total * 100)
    bd_rate = round(breakdown / total * 100)
    bu_rate = round(backup / total * 100)

    server_number = Server.objects.count()
    networkdevice_number = NetworkDevice.objects.count()
    storagedevice_number = StorageDevice.objects.count()
    securitydevice_number = SecurityDevice.objects.count()
    software_number = Software.objects.count()

    return render(request, 'assets/dashboard.html', locals())
