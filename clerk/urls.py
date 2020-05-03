from django.urls import path

from . import views


app_name = 'clerk'

urlpatterns = [
    path('adfajklkdsf/acc99qjia9345j/sfa93lkfa/32rk/a93n/r', views.signup, name='signup'),
    path('', views.login, name='login'),
    path('function/', views.index, name='index'),
    path('function/0/', views.index),

    # book_editing
    path('function/1/', views.book_edit_view),
    path('function/1/0/', views.book_edit_view, name='book_edit_view'),
    # path('function/1/0/<str:isbn>/', views.do_edit, name='book_edit_form'),
    # path('function/1/1/', views.add_category, name='add_category'),

    # add import order
    # book detail
    path('function/2/', views.import_order_view),
    path('function/2/0/', views.import_order_view, name='import_order_view'),
    # cart-detail
    path('function/2/1/', views.order_detail, name='order_detail'),
    path('function/2/1/delete/<str:isbn>/', views.drop_order, name='drop_order'),
    # path('function/2/1/submit-order', views.submit_order, name='submit_order'),

    # cart detail template
    path('function/3/', views.check_finance_detail),
    path('function/3/0/', views.check_finance_detail, name='check_finance_detail'),

    # maybe User manage **
    # maybe clerk manage *
    # maybe account manage ***

    # logout
    path('logout/', views.logout, name='logout')
]