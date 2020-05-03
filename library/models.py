from django.db import models


# from login.models import User


# Create your models here.
class Category(models.Model):
    cate_id = models.PositiveSmallIntegerField(primary_key=True, verbose_name='category id')
    name = models.CharField(unique=True, max_length=256)

    class Meta:
        ordering = ['cate_id']


class Books(models.Model):
    # need check ISBN == 11
    ISBN = models.CharField(primary_key=True, max_length=11)
    title = models.CharField(max_length=100)
    # maybe more than 1 author.... I don't care
    author = models.CharField(max_length=100, default='anonymous')
    publisher = models.CharField(max_length=100, default='anonymous')
    publish_date = models.DateField()
    advertise = models.CharField(max_length=1000)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    inventory = models.IntegerField(default=0)
    cover = models.FileField(upload_to='static/common/book_cover')

    cate_id = models.ForeignKey(Category, models.CASCADE, default={'cate_id': 0})
