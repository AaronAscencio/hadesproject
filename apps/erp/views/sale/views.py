from django.forms.models import model_to_dict
from django.db import transaction
from django.http.response import JsonResponse
from django.shortcuts import render
import json
from django.urls import reverse_lazy
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,FormView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from apps.erp.mixins import IsSuperuserMixin,ValidatePermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin


from apps.erp.models import *
from apps.erp.forms import CategoryForm, SaleForm


class SaleCreateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,CreateView):
    permission_required = 'erp.add_sale'
    model = Sale
    form_class = SaleForm
    template_name = 'sale/create.html'
    success_url = reverse_lazy('index_view')

    def get_context_data(self,**kwargs):
        context =  super().get_context_data(**kwargs)
        context['title'] = 'Creacion de una Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = reverse_lazy('erp:category_list')
        context['action'] = 'add'
        return context


    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    
    def post(self,request,*args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if(action=='search_product'):
                data=[]
                products = Product.objects.filter(name__icontains=request.POST['term'])[0:10]
                for i in products:
                    item = i.toJSON()
                    item['value'] = i.name
                    data.append(item)
            elif(action=='add'):
                vents = json.loads(request.POST['vents'])
                with transaction.atomic():
                    sale = Sale()
                    sale.date_joined = vents['date_joined']
                    sale.cli_id = vents['cli']
                    sale.subtotal = float(vents['subtotal'])
                    sale.iva = float(vents['iva'])
                    sale.total = float(vents['total'])
                    sale.save()
                    for i in vents['products']:
                        det = DetSale()
                        det.sale_id = sale.id
                        det.prod_id = i['id']
                        det.cant = int(i['cant'])
                        det.price = float(i['pvp'])
                        det.subtotal = float(i['subtotal'])
                        det.save()



            else:
                data['error'] = 'No se ha enviado ninguna accion'
        except Exception as e:
            data['error'] = str(e)
            
        return JsonResponse(data,safe=False)