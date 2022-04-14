from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.http import JsonResponse

from apps.reports.forms import ReportForm
from apps.erp.models import Sale
# Create your views here.

class ReportSaleView(TemplateView):
    template_name = 'sale/report.html'


    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Ventas'
        context['entity'] = 'Reportes'
        context['list_url'] = reverse_lazy('reports:sale_report')
        context['form'] = ReportForm()
        return context  


    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if(action == 'search_report'):
                data = []
                start_date = request.POST.get('start_date','')
                end_date = request.POST.get('end_date','')
                search = Sale.objects.all()
                if(len(start_date) and len(end_date)):
                    search = search.filter(date_joined__range=[start_date,end_date])
                for s in search:
                    data.append([
                        s.id,
                        s.cli.names,
                        s.date_joined.strftime('%Y-%m-%d'),
                        format(s.subtotal,'.2f'),
                        format(s.iva,'.2f'),
                        format(s.total,'.2f'),
                    ])



            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)