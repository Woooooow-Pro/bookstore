from django.db import models


# Create your models here.
class Finance(models.Model):
    class role(enumerate):
        user = 1
        clerk = 2

    class func(enumerate):
        sold = 1
        buy = 2

    function = models.IntegerField(null=False, default=func.sold)
    executor_role = models.IntegerField(null=False, default=role.user)
    sum = models.DecimalField(null=False, decimal_places=2, max_digits=10, default=0)
    date = models.DateField(auto_now_add=True)
    person_id = models.CharField(max_length=30, null=False, default='missing')

    class Meta:
        ordering = ['date']