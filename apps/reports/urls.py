from django.urls import path
from apps.reports.views import *

app_name = 'reports'

urlpatterns = [
     #Reports
     path('sale/',ReportSaleView.as_view(),name='sale_report')
]
