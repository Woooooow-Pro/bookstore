from django.db import models
from library.models import Books
from finance.models import Finance


# Create your models here.
class Clerk(models.Model):
    sex = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    )

    clerk_id = models.CharField(max_length=11, primary_key=True)
    password = models.CharField(max_length=256, default='SBPJ')
    salt = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=11, unique=True)
    gender = models.CharField(max_length=10, choices=sex, default='Male')
    c_time = models.TimeField(auto_now_add=True)
    active = models.BooleanField(null=False, default=False)

    def default_password(self):
        return 'sbpj'+self.clerk_id


# add by super user
class Role(models.Model):
    role_name = models.CharField(max_length=256)
    menu_name = models.CharField(max_length=256, null=False, default='Edit Book', unique=True)
    role_menu_url = models.CharField(max_length=256, null=False, default='1')
    info = models.TextField()

    def get_sub_menu(self):
        sub_menu_list = Permission_cate.objects.filter(role=self)
        return sub_menu_list


class Permission_cate(models.Model):
    role = models.ForeignKey(Role, models.CASCADE)
    sub_menu_url = models.CharField(max_length=10)
    name = models.CharField(max_length=256)


# many to many model
class Clerk_Role(models.Model):
    clerk = models.ForeignKey(Clerk, models.CASCADE)
    role = models.ForeignKey(Role, models.CASCADE)


class Import_Order(models.Model):
    clerk = models.ForeignKey(Clerk, models.DO_NOTHING)
    book = models.ForeignKey(Books, models.DO_NOTHING)
    import_price = models.DecimalField(decimal_places=2, max_digits=10)
    quantity = models.IntegerField(default=10)


# add to cart
def add_import_order(clerk, book, number, price):
    try:
        import_order = Import_Order.objects.get(book=book, clerk=clerk)
        import_order.quantity += number
        import_order.save()
    except Import_Order.DoesNotExist:
        new_order = Import_Order.objects.create(book=book, clerk=clerk, import_price=price, quantity=number)
        new_order.save()


# pay
def submit_order(clerk):
    orders = Import_Order.objects.filter(clerk=clerk)
    total = 0
    for order in orders:
        total += order.quantity * order.import_price
        order.book.inventory += order.quantity
        order.book.save()
        order.delete()

    finance = Finance.objects.create()
    finance.function = finance.func.buy
    finance.executor_role = finance.role.clerk
    finance.sum = total
    finance.person_id = clerk.clerk_id
    finance.save()


# remove from cart
def remove_from_order(clerk, book):
    try:
        order = Import_Order.objects.get(book=book, clerk=clerk)
        order.delete()
    except Import_Order.DoesNotExist:
        pass


# get all order
def get_all_import_order(clerk):
    orders = Import_Order.objects.filter(clerk=clerk)
    return orders
