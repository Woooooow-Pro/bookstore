from django.db import transaction
from django.shortcuts import render, redirect
from .models import Books, Category
from login.models import User
from login.views import check_login
from django.db.models import Q


# Create your views here.
def index(request):
    check_login(request)
    books = get_list_by_cate(0)
    category = get_all_cate()
    return render(request, 'library/index.html', locals())


def list_by_cate(request, cid=0):
    check_login(request)

    category = get_all_cate()
    books = get_list_by_cate(cid)

    # print(books[0].cover)

    return render(request, 'library/store.html', locals())


def search_result(request):
    check_login(request)
    category = get_all_cate()
    key = request.POST['keyword']
    if len(key):
        books = Books.objects.filter(Q(ISBN__contains=key) | Q(title__contains=key) | Q(author__contains=key) | Q(publisher__contains=key))
    else:
        books = Books.objects.all()
    return render(request, 'library/search_result.html', locals())


# book_detail.html 实现
def book_detail(request, ISBN):
    check_login(request)

    if len(ISBN) != 11:
        return redirect('library:index')
    try:
        book = Books.objects.get(ISBN=ISBN)
    except Books.DoesNotExist:
        return redirect('library:index')
    else:
        context = {
            'book': book
        }
        return render(request, 'library/book_detail.html', context)


@transaction.atomic
def add_to_cart(request, isbn):
    check_login(request)
    amount = int(request.POST['amount'])
    if amount <= 0:
        return redirect('library:book_detail')

    book = Books.objects.get(ISBN=isbn)
    user = User.objects.get(username=request.session['username'])
    user.add_to_cart(book, amount)
    return redirect('library:index')


# cart.html 实现
def cart_contain(request):
    check_login(request)
    category = get_all_cate()
    user = User.objects.get(username=request.session['username'])
    orders = user.get_all_order()
    return render(request, 'library/cart.html', locals())


def cat_drop(request, isbn):
    check_login(request)
    user = User.objects.get(username=request.session['username'])
    try:
        book = Books.objects.get(ISBN=isbn)
        user.remove_from_order(book)
    except Books.DoesNotExist:
        pass
    return redirect('library:cart')


@transaction.atomic
def do_pay(request):
    check_login(request)
    username = request.session['username']
    user = User.objects.get(username=username)
    user.pay()
    return redirect('library:index')


def get_all_cate():
    cate = Category.objects.all()
    return cate


def get_list_by_cate(cid):
    if cid:
        try:
            cate = Category.objects.get(cate_id=cid)
        except Category.DoesNotExist:
            books = Books.objects.all()
        else:
            books = Books.objects.filter(cate_id=cate)
    else:
        books = Books.objects.all()
    return books


def get_summary(orders):
    total = 0
    for order in orders:
        total += order.book.price * order.quantity
    return total
