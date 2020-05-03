from django.db import models
from library.models import Books
from finance.models import Finance


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=30, primary_key=True)
    password = models.CharField(max_length=256)
    salt = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=11, unique=True)
    # city = models.CharField(max_length=100)
    # street = models.CharField(max_length=100)
    c_time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    def add_to_cart(self, book, number):
        try:
            order = BookOrder.objects.get(book=book, cart=self)
            order.quantity += number
            order.save()
        except BookOrder.DoesNotExist:
            new_order = BookOrder.objects.create(book=book, cart=self, quantity=number)
            new_order.save()

    # 还没加入
    def remove_from_order(self, book):
        try:
            order = BookOrder.objects.get(book=book, cart=self)
            order.delete()
        except BookOrder.DoesNotExist:
            pass

    def total(self):
        orders = BookOrder.objects.filter(cart=self)
        total = 0
        count = 0
        for order in orders:
            total += order.book.price * order.quantity
            count += order.quantity
        context = {
            'total': total,
            'count': count
        }
        return context

    def get_all_order(self):
        orders = BookOrder.objects.filter(cart=self)
        return orders

    def pay(self):
        orders = BookOrder.objects.filter(cart=self)
        total = 0
        for order in orders:
            total += order.book.price * order.quantity
            order.book.inventory -= order.quantity
            order.book.save()
            order.delete()

        finance = Finance.objects.create()
        finance.function = finance.func.sold
        finance.executor_role = finance.role.user
        finance.sum = total
        finance.person_id = self.username
        finance.save()

    class Meta:
        ordering = ['c_time']


class BookOrder(models.Model):
    book = models.ForeignKey(Books, models.CASCADE)
    cart = models.ForeignKey(User, models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
