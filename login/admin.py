from django.contrib import admin
from . import models
from library.models import Category

admin.site.register(models.User)
admin.site.register(models.BookOrder)
admin.site.register(models.Books)
admin.site.register(Category)
# Register your models here.
