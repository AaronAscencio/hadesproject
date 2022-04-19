
from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import FloatField,Sum
from django.db.models.functions import Coalesce
from datetime import datetime



from apps.erp.models import Sale
# Create your views here.



class IndexView(TemplateView):

    def get_graph_sales_year_month(self):
        data = []
        try:
            year = datetime.now().year
            for m in range(1,13):
                total = Sale.objects.filter(date_joined__year=year, date_joined__month=m).aggregate(r=Coalesce(Sum('total'), 0, output_field=FloatField())).get('r')
                data.append(float(total))
        except Exception as e:
            print(str(e))
        return data

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['graph_sales_year_month'] = self.get_graph_sales_year_month()
        return context

    template_name = 'index.html'


