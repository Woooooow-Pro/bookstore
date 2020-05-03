from django.shortcuts import render, redirect
from .models import Finance


def finance_summary():
    finances = Finance.objects.all()
    sold = 0
    buy = 0
    for f in finances:
        if f.function == f.func.sold:
            sold += f.sum
        else:
            buy += f.sum
    total = {
        'sold': sold,
        'buy': buy
    }
    return total


