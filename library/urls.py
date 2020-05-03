from django.urls import path, include
from . import views
app_name = 'library'

urlpatterns = [
    path('', views.index, name='index'),
    # path('category/', views.all_book),
    path('category/<int:cid>/', views.list_by_cate, name='list_by_cate'),
    path('books/<str:ISBN>', views.book_detail, name='book_detail'),
    path('search-result', views.search_result, name='search_result'),
    path('addto-cart/<str:isbn>', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_contain, name='cart'),
    path('pay/', views.do_pay, name='pay'),
]
