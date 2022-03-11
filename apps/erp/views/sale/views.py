from django.forms.models import model_to_dict
from django.db import transaction
from django.http import HttpResponse,HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
import json
from django.urls import reverse_lazy
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,FormView,View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from pkg_resources import safe_extra
from apps.erp.mixins import IsSuperuserMixin,ValidatePermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin

#xhtml2pdf
from django.contrib.staticfiles import finders
import os
from django.conf import settings
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from io import BytesIO
from xhtml2pdf import pisa


from apps.erp.models import *
from apps.erp.forms import CategoryForm, SaleForm


class SaleCreateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,CreateView):
    permission_required = 'erp.add_sale'
    model = Sale
    form_class = SaleForm
    template_name = 'sale/create.html'
    success_url = reverse_lazy('erp:sale_list')

    def get_context_data(self,**kwargs):
        context =  super().get_context_data(**kwargs)
        context['title'] = 'Creacion de una Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = reverse_lazy('erp:category_list')
        context['action'] = 'add'
        context['det'] = []
        return context


    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    
    def post(self,request,*args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if(action=='search_products'):
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
                    data = {'id':sale.id}


            else:
                data['error'] = 'No se ha enviado ninguna accion'
        except Exception as e:
            data['error'] = str(e)
            
        return JsonResponse(data,safe=False)

class SaleListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Sale
    template_name = 'sale/list.html'
    permission_required = 'erp.view_sale'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Sale.objects.all():
                    data.append(i.toJSON())
            elif(action=='search_details_prod'):
                data = []
                for i in DetSale.objects.filter(sale_id=request.POST['id']):
                    data.append(i.toJSON())
            
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Ventas'
        context['create_url'] = reverse_lazy('erp:sale_create')
        context['list_url'] = reverse_lazy('erp:sale_list')
        context['entity'] = 'Ventas'
        return context

class SaleDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Sale
    template_name = 'sale/delete.html'
    success_url = reverse_lazy('erp:sale_list')
    permission_required = 'erp.delete_sale'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de una Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        return context


class SaleUpdateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,UpdateView):
    permission_required = 'erp.change_sale'
    model = Sale
    form_class = SaleForm
    template_name = 'sale/create.html'
    success_url = reverse_lazy('erp:sale_list')


    def get_details_products(self):
        data = []
        try:
            for i in DetSale.objects.filter(sale_id=self.get_object().id):
                item = i.prod.toJSON()
                item['cant'] = i.cant 
                data.append(item)

        except:
            pass
        data = json.dumps(data)
        return data

    def get_context_data(self,**kwargs):
        context =  super().get_context_data(**kwargs)
        context['title'] = 'Creacion de una Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = reverse_lazy('erp:category_list')
        context['action'] = 'edit'
        context['det'] = self.get_details_products()
        return context


    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    
    def post(self,request,*args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if(action=='search_products'):
                data=[]
                products = Product.objects.filter(name__icontains=request.POST['term'])[0:10]
                for i in products:
                    item = i.toJSON()
                    item['value'] = i.name
                    data.append(item)
            elif(action=='edit'):
                vents = json.loads(request.POST['vents'])
                with transaction.atomic():
                    sale = Sale.objects.get(id=self.get_object().id)
                    sale.date_joined = vents['date_joined']
                    sale.cli_id = vents['cli']
                    sale.subtotal = float(vents['subtotal'])
                    sale.iva = float(vents['iva'])
                    sale.total = float(vents['total'])
                    sale.save()
                    sale.detsale_set.all().delete()
                    for i in vents['products']:
                        det = DetSale()
                        det.sale_id = sale.id
                        det.prod_id = i['id']
                        det.cant = int(i['cant'])
                        det.price = float(i['pvp'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
                    data = {'id':sale.id}


            else:
                data['error'] = 'No se ha enviado ninguna accion'
        except Exception as e:
            data['error'] = str(e)
            
        return JsonResponse(data,safe=False)


class SaleInvoicePdfView(View):

    def link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        # use short variable names
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /static/media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        # convert URIs to absolute system paths
        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri  # handle absolute uri (ie: http://some.tld/foo.png)

        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path
    
    def get(self,request,*args,**kwargs):
        try:
            s = Sale.objects.get(pk = self.kwargs['pk'])
            context = {'sale':Sale.objects.get(pk = self.kwargs['pk']),
                'comp':{'name':'Alogorisoft SA de CV','ruc':'9999999999999','address':'Milagro, Ecuador'},
                'icon': '{}{}'.format(settings.STATIC_URL, 'img/logo.png')
            }
            template = get_template('sale/invoice.html')
            response = HttpResponse(content_type='application/pdf')
            html = template.render(context)
            #response['Content-Disposition'] = f'attachment; filename="No_{s.id}_Report.pdf"'
            pisaStatus = pisa.CreatePDF(
                html, dest=response,
                link_callback=self.link_callback
            )
            # if error then show some funy view
            return response
        except Exception as e:
            print(str(e))
        return HttpResponseRedirect(reverse_lazy('erp:sale_list'))