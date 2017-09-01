from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import PasswordChangeForm
# Create your views here.
#主页 登录 登出
def index(request):
    return render(request, 'index.html')

def acc_login(request):
    err_msg = ''
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            err_msg = "Wrong username or password"
    return render(request, 'login.html', {'err_msg':err_msg})

def acc_logout(request):
    logout(request)
    return redirect('index')

def change_pwd(request):
    err_msg = ''
    success_msg = ''
    if request.method == "POST":
        username = request.user.username
        oldpwd = request.POST.get('oldpassword')
        newpwd = request.POST.get('newpassword')
        newpwd2 = request.POST.get('newpassword2')
        user = authenticate(username=username,password=oldpwd)
        if user is not None:
            if newpwd == newpwd2:
                user.set_password(newpwd)
                user.save()
                success_msg = "密码修改成功"
            else:
                err_msg = "两次密码不一致"
        else:
            err_msg = "原密码输入错误"
    return render(request, 'changepwd.html', {'err_msg':err_msg, 'success_msg':success_msg})