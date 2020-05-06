from django.db import transaction
from django.shortcuts import render, redirect
from . import models
import hashlib
import random
import string


# Create your views here.
@transaction.atomic
def sign_up(req):
    if req.session.get('has_login'):
        redirect('library:index')

    flag = True
    if req.method == 'POST':
        username = req.POST.get('username')

        password = req.POST.get('password')

        email = req.POST.get('email')

        phone = req.POST.get('phone')

        # print(username)
        # print(password)
        # print(email)
        # print(phone)

        same_name_user1 = models.User.objects.filter(username=username)
        same_name_user2 = models.User.objects.filter(email=email)
        same_name_user3 = models.User.objects.filter(phone=phone)
        if same_name_user1.count():
            message1 = "username Has Been Used"
            flag = False
        if same_name_user2.count():
            message2 = "Email Has Been Used"
            flag = False
        if same_name_user3.count():
            message3 = "Phone Has Been Used"
            flag = False
        if flag:
            salt = rand_str()
            hs = hashlib.md5()
            password += salt
            hs.update(password.encode())

            user = models.User.objects.create()
            user.password = hs.hexdigest()
            user.salt = salt
            user.username = username
            user.phone = phone
            user.email = email
            user.save()
            return redirect('login:login')
    return render(req, 'signup.html', locals())


def login(req):
    if req.session.get('has_login'):
        return redirect('library:index')
    if req.method == 'POST':
        username = req.POST['username']
        user = None
        user1 = models.User.objects.filter(username=username)
        if user1.count() == 0:
            user1 = models.User.objects.filter(phone=username)
            if user1.count() == 0:
                user1 = models.User.objects.filter(email=username)
        if user1.count():
            user = user1[0]
        else:
            message1 = "User do not exist"
            return render(req, "login.html", locals())

        password = req.POST['password']
        # req.session['password'] = password
        password += user.salt
        hs = hashlib.md5(password.encode())
        if user.password == hs.hexdigest():
            req.session['has_login'] = True
            req.session['username'] = username
            return redirect('library:index')
        message2 = "Wrong Password"
    return render(req, "login.html", locals())


def logout(request):
    if request.session['has_login'] is None:
        return redirect('login:login')
    request.session.flush()
    return redirect('login:login')


def rand_str():
    salt = ''.join(random.sample(string.ascii_letters + string.digits, 28))
    return salt


def check_login(request):
    if request.session.get('has_login', None) and request.session.get('clerk_login', None):
        return redirect('login:login')


