from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from apps.reports.forms import ReportForm
# Create your views here.

class ReportSaleView(TemplateView):
    template_name = 'sale/report.html'


    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Ventas'
        context['entity'] = 'Reportes'
        context['list_url'] = reverse_lazy('reports:sale_report')
        context['form'] = ReportForm()
        return context