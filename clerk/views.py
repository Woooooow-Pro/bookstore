from django.db import transaction
from django.db.models import Q
from django.shortcuts import render, redirect
from .models import Clerk, Role, Import_Order, Clerk_Role, \
    add_import_order, \
    get_all_import_order, \
    submit_order, \
    remove_from_order
from login.views import rand_str
from library.views import get_all_cate
from library.models import Books, Category
from finance.models import Finance
from finance.views import finance_summary
import hashlib
from django.utils.datastructures import MultiValueDictKeyError


# Create your views here.
@transaction.atomic
def login(req):
    if req.session.get('has_login'):
        return redirect('library:index')
    if req.session.get('clerk_login'):
        return redirect('clerk:index')

    if req.method == 'POST':
        clerk_id = req.POST['clerk_id']
        password = req.POST['password']
        try:
            clerk = Clerk.objects.get(clerk_id=clerk_id)
        except Clerk.DoesNotExist:
            return redirect('login:login')

        if password == clerk.default_password() and (not clerk.active) and clerk.password == 'SBPJ':
            req.session['clerk_id'] = clerk_id
            return redirect('clerk:signup')

        if not clerk.active:
            warning = '你的账号被限制访问了'
            return render(req, 'clerk/login.html', locals())

        password += clerk.salt
        hs = hashlib.md5(password.encode())
        if clerk.password == hs.hexdigest():
            req.session['clerk_login'] = True
            req.session['clerk_id'] = clerk_id
            return redirect('clerk:index')
        message = "Wrong Password"
    return render(req, "clerk/login.html", locals())


@transaction.atomic
def signup(request):
    if request.session.get('has_login'):
        return redirect('library:index')
    if request.session.get('clerk_login'):
        return redirect('clerk:index')
    if request.method == 'POST':
        if request.session.get('clerk_id'):
            clerk_id = request.session['clerk_id']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            clerk = Clerk.objects.get(clerk_id=clerk_id)
            if password1 == password2:
                password = password1
                salt = rand_str()
                hs = hashlib.md5()
                password += salt
                hs.update(password.encode())
                clerk.salt = salt
                clerk.password = hs.hexdigest()
                clerk.active = True
                clerk.save()
                return redirect('clerk:login')
            else:
                message = '两次密码不一致'
                return render(request, 'clerk/signup.html', locals())
        else:
            return redirect('login:login')
    return render(request, 'clerk/signup.html', locals())


# finance summary
def index(request):
    clerk_login(request)
    roles = get_all_permission(request)
    # print(roles)
    finance_total = finance_summary()
    sold = finance_total['sold']
    buy = finance_total['buy']
    return render(request, 'clerk/index.html', locals())


# 以下所有函数都还没有判断 clerk 级别
# book-editing
@transaction.atomic
def book_edit_view(request):
    clerk_login(request)

    roles = get_all_permission(request)
    category = get_all_cate()
    if request.method == 'POST':
        try:
            key = request.POST['keyword']
            if len(key) > 0:
                books = Books.objects.filter(
                    Q(ISBN__contains=key) | Q(title__contains=key) | Q(author__contains=key) | Q(
                        publisher__contains=key)).order_by('inventory')
                return render(request, 'clerk/book_edit.html', locals())
        except KeyError:
            isbn = request.POST['isbn']
            title = request.POST['title']
            author = request.POST['author']
            publisher = request.POST['publisher']
            publish_date = request.POST['publish_date']
            advertise = request.POST['advertise']
            price = request.POST['price']
            cate_id = Category.objects.get(cate_id=request.POST['cate'])
            cover = request.FILES['cover']
            print(cate_id)
            try:
                book = Books.objects.get(ISBN=request.POST['isbn'])
                book.title = title
                book.author = author
                book.advertise = advertise
                book.publisher = publisher
                book.publish_date = publish_date
                book.price = price
                book.cover = cover
                book.cate_id = cate_id
                book.save()
            except Books.DoesNotExist:
                book = Books.objects.create(
                    ISBN=isbn,
                    title=title,
                    author=author,
                    advertise=advertise,
                    publisher=publisher,
                    publish_date=publish_date,
                    price=price,
                    cover=cover,
                    cate_id=cate_id
                )
                book.save()
            return redirect('clerk:book_edit_view')
    books = Books.objects.all().order_by('inventory')
    return render(request, 'clerk/book_edit.html', locals())


@transaction.atomic
def do_edit(request, isbn):
    clerk_login(request)
    roles = get_all_permission(request)
    category = get_all_cate()
    try:
        book = Books.objects.get(ISBN=isbn)
    except Books.DoesNotExist:
        return redirect('clerk:book_edit_view')
    if request.method == 'POST':
        book.title = request.POST['title']
        book.author = request.POST['author']
        book.publisher = request.POST['publisher']
        book.publish_date = request.POST['publish_date']
        book.advertise = request.POST['advertise']
        book.price = request.POST['price']
        book.cate_id = Category.objects.get(cate_id=request.POST['cate'])
        cover = request.FILES['cover']
        book.cover = cover
        # print(cate_id)
        # book.title = title
        # book.author = author
        # book.advertise = advertise
        # book.publisher = publisher
        # book.publish_date = publish_date
        # book.price = price
        # book.cover = cover
        # book.cate_id = cate_id
        book.save()
        return redirect('clerk:book_edit_view')
    return render(request, 'clerk/do-edit.html', locals())


@transaction.atomic
def import_order_view(request):
    clerk_login(request)
    roles = get_all_permission(request)
    category = get_all_cate()
    if request.method == 'POST':
        try:
            key = request.POST['keyword']
            if len(key):
                books = Books.objects.filter(
                    Q(ISBN__contains=key) | Q(title__contains=key) | Q(author__contains=key) | Q(
                        publisher__contains=key)).order_by('inventory')
                return render(request, 'clerk/import_order_view.html', locals())
        except KeyError:
            book = Books.objects.get(ISBN=request.POST['isbn'])
            quantity = int(request.POST['quantity'])
            price = float(request.POST['price'])
            if quantity <= 0:
                return redirect('clerk:import_order_view')
            clerk = Clerk.objects.get(clerk_id=request.session['clerk_id'])
            add_import_order(clerk, book, quantity, price)
            return redirect('clerk:import_order_view')
    books = Books.objects.all().order_by('inventory')
    return render(request, 'clerk/import_order_view.html', locals())


# 包括了提交订单（到现在才有点明白自己在干啥，我裂开啦~）
@transaction.atomic
def order_detail(request):
    clerk_login(request)
    clerk = Clerk.objects.get(clerk_id=request.session['clerk_id'])
    roles = get_all_permission(request)
    if request.method == 'POST':
        try:
            key = request.POST['keyword']
            if len(key):
                books = Books.objects.filter(Q(ISBN__contains=key) | Q(title__contains=key) | Q(author__contains=key) | Q(
                        publisher__contains=key))
                orders = Import_Order.objects.filter(book__in=books)
                return render(request, 'clerk/order_detail.html', locals())
        except KeyError:
            submit_order(clerk)
            return redirect('clerk:order_detail')

    orders = get_all_import_order(clerk)
    return render(request, 'clerk/order_detail.html', locals())


@transaction.atomic
def drop_order(request, isbn):
    clerk_login(request)
    clerk = Clerk.objects.get(clerk_id=request.session['clerk_id'])
    try:
        book = Books.objects.get(ISBN=isbn)
        remove_from_order(clerk, book)
    except Books.DoesNotExist:
        pass
    return redirect('clerk:order_detail')


def check_finance_detail(request):
    clerk_login(request)
    roles = get_all_permission(request)
    finances_import = Finance.objects.filter(function=2).order_by('date')
    finances_sold = Finance.objects.filter(function=1).order_by('date')
    return render(request, 'clerk/finance_detail.html', locals())


@transaction.atomic
def clerk_manage(request):
    clerk_login(request)
    clerks = Clerk.objects.all().order_by('c_time')
    roles = Role.objects.all()
    if request.method == 'POST':
        clerk_id = request.POST['clerk_id']
        phone = request.POST['phone']
        email = request.POST['email']
        gender = request.POST['gender']
        try:
            clerk = Clerk.objects.get(clerk_id=clerk_id)
            message = 'Clerk Id Has Been Used'
            return render(request, 'clerk/clerk_manage_view.html', locals())
        except Clerk.DoesNotExist:
            c = Clerk.objects.create(
                clerk_id=clerk_id,
                phone=phone,
                email=email,
                gender=gender
            )
            c.save()
    return render(request, 'clerk/clerk_manage_view.html', locals())


@transaction.atomic
def clerk_edit(request, clerk_id):
    clerk_login(request)
    clerk_id = str(clerk_id)
    clerk = Clerk.objects.get(clerk_id=clerk_id)
    roles = Role.objects.all()
    clerk_roles = Clerk_Role.objects.filter(clerk=clerk)
    clerk_delete = []
    clerk_add = []
    for cr in clerk_roles:
        clerk_delete.append(cr.role)
    for r in roles:
        if r not in clerk_delete:
            clerk_add.append(r)

    if request.method == 'POST':
        clerk.phone = request.POST['phone']
        clerk.email = request.POST['email']
        # clerk.gender = request.POST['gender']
        try:
            request.POST['active'] == 'TRUE'
            clerk.active = True
        except MultiValueDictKeyError:
            clerk.active = False
        clerk.save()
        try:
            if request.POST['add_menu_url'] == 'x':
                pass
            else:
                role_add = Role.objects.get(role_menu_url=request.POST['add_menu_url'])
                clerk_role_add = Clerk_Role.objects.create(role=role_add, clerk=clerk)
                clerk_role_add.save()
        except MultiValueDictKeyError:
            pass
        try:
            if request.POST['del_menu_url'] == 'x':
                pass
            else:
                role_del = Role.objects.get(role_menu_url=request.POST['del_menu_url'])
                clerk_role_del = Clerk_Role.objects.get(role=role_del, clerk=clerk)
                clerk_role_del.delete()
        except MultiValueDictKeyError:
            pass

        return redirect('clerk:clerk_manage')
    return render(request, 'clerk/clerk_edit.html', locals())


# 一些测试函数
def clerk_login(request):
    if request.session.get('has_login'):
        return redirect('library:index')
    if request.session.get('clerk_login', None):
        return redirect('clerk:login')


def get_all_permission(request):
    clerk = Clerk.objects.get(clerk_id=request.session['clerk_id'])
    clerk_role = Clerk_Role.objects.filter(clerk=clerk)
    role = []
    for cr in clerk_role:
        role.append(cr.role)
    role.sort(key=sort_key)
    return role


def sort_key(role):
    return role.role_menu_url


def logout(request):
    if request.session['clerk_login'] is None:
        return redirect('login:login')
    request.session.flush()
    return redirect('clerk:login')
