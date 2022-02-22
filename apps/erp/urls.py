

from django.urls import path

from apps.erp.views.category.views import *
from apps.erp.views.products.views import *
from apps.erp.views.client.views import *
from apps.erp.views.test.views import *
from apps.erp.views.sale.views import *
app_name = 'erp'

urlpatterns = [ 
    #Categories
    path('category/list/',CategoryListView.as_view(),name="category_list"),
    path('category/add/',CategoryCreateView.as_view(),name="category_create"),
    path('category/update/<int:pk>/',CategoryUpdateView.as_view(),name="category_update"),
    path('category/delete/<int:pk>/',CategoryDeleteView.as_view(),name="category_delete"),
    path('category/form/',CategoryFormView.as_view(),name="category_form"),
    #Products
    path('product/list/',ProductListView.as_view(),name="product_list"),
    path('product/add/',ProductCreateView.as_view(),name="product_create"),
    path('product/delete/<int:pk>/',ProductDeleteView.as_view(),name="product_delete"),
    path('product/update/<int:pk>/',ProductUpdateView.as_view(),name="product_update"),


    #Clients
    path('client/list',ClientView.as_view(),name="client_list"),
    #Test
    path('test/select_view/',SelectView.as_view(),name="test_select"),

    #Sale
    path('sale/add/',SaleCreateView.as_view(),name="sale_create"),
    path('sale/list/',SaleListView.as_view(), name='sale_list'),
    path('sale/delete/<int:pk>/', SaleDeleteView.as_view(), name='sale_delete'),
]