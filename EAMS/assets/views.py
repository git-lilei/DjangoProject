from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
# Create your views here.
from django.shortcuts import get_object_or_404
from .models import *
from .forms import *

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


# 添加资产
def add(request):
    if request.method == 'GET':
        add_form = AddForm()
        return render(request, 'assets/add.html', locals())
    elif request.method == 'POST':
        message = '请检查填写内容'
        add_form = AddForm(request.POST)
        if add_form.is_valid():
            asset_type = add_form.cleaned_data['asset_type']
            name = add_form.cleaned_data['name']
            sn = add_form.cleaned_data['sn']
            manufacturer = add_form.cleaned_data['manufacturer']
            status = add_form.cleaned_data['status']
            idc = add_form.cleaned_data['idc']
            purchase_day = add_form.cleaned_data['purchase_day']

            same_sn = Asset.objects.filter(sn=sn)
            if same_sn:
                message = '该设备已存在'
                return render(request, 'assets/add.html', locals())

            new_asset = Asset()
            new_asset.asset_type = asset_type
            new_asset.name = name
            new_asset.sn = sn
            new_asset.manufacturer = manufacturer
            new_asset.status = status
            new_asset.idc = idc
            new_asset.purchase_day = purchase_day
            new_asset.save()
            message = '添加成功'

            return redirect(reverse('assets:index'))


# 修改资产
def edit(request, asset_id):
    if request.method == 'GET':
        asset = Asset.objects.get(pk=asset_id)
        form = EditForm(
            initial={
                'asset_type': asset.asset_type,
                'name': asset.name,
                'sn': asset.sn,
                'manufacturer': asset.manufacturer,
                'status': asset.status,
                'idc': asset.idc,
                'purchase_day': asset.purchase_day,
            }
        )
        return render(request, 'assets/edit.html', {'Edit_FormInput': form})
    elif request.method == 'POST':
        edit_form = EditForm(request.POST)
        if edit_form.is_valid():
            asset_type = edit_form.cleaned_data['asset_type']
            name = edit_form.cleaned_data['name']
            sn = edit_form.cleaned_data['sn']
            manufacturer = edit_form.cleaned_data['manufacturer']
            status = edit_form.cleaned_data['status']
            idc = edit_form.cleaned_data['idc']
            purchase_day = edit_form.cleaned_data['purchase_day']

            edit_asset = Asset.objects.get(pk=asset_id)
            edit_asset.asset_type = asset_type
            edit_asset.name = name
            edit_asset.sn = sn
            edit_asset.manufacturer = manufacturer
            edit_asset.status = status
            edit_asset.idc = idc
            edit_asset.purchase_day = purchase_day
            edit_asset.save()

            return redirect(reverse('assets:index'))
        else:
            return redirect(reverse('assets:edit', args=str(asset_id)))


# 删除资产
def del_asset(request, asset_id):
    try:
        del_asset = Asset.objects.get(pk=asset_id)
        del_asset.delete()
        return redirect(reverse('assets:index'))
    except:
        return redirect(reverse('assets:index'))