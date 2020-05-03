from django.contrib import admin
from finance.models import Finance
from .models import Clerk, Clerk_Role, Role, Permission_cate, Import_Order

# Register your models here.
admin.site.register(Finance)
admin.site.register(Clerk_Role)
admin.site.register(Clerk)
admin.site.register(Role)
admin.site.register(Permission_cate)
admin.site.register(Import_Order)




