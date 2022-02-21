from django.views.generic import TemplateView
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import  login_required
from django.forms import *

from apps.erp.forms import TestForm
from apps.erp.models import Category, Product


class SelectView(TemplateView):
    template_name = 'test.html'


    @method_decorator(csrf_exempt)
   
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Selects | Anidados con Ajax'
        context['entity'] = 'Test'
        context['form'] = TestForm()
        return context


    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_product_id':
                data = [{'id':'','text':'--------'}]
                c = Category.objects.get(pk=request.POST['id'])
                for i in Product.objects.filter(cate=c):
                    data.append({'id':i.id,'text':i.name})
            elif(action == 'autocomplete'):
                data = []
                for i in Category.objects.filter(name__icontains = request.POST['term'])[0:5]:
                    item = model_to_dict(i)
                    item['value'] = i.name
                    data.append(item)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    