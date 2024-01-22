from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader
from .models import DoorBlock

from urllib.parse import quote, unquote


def index(request):
        door_block_list = DoorBlock.objects.all()
        template = loader.get_template('polls/index.html')
        if 'door_table' in request.COOKIES.keys():
            door_table = unquote(request.COOKIES['door_table'])
        else:
            door_table = []
        context = {
            'door_block_list': door_block_list,
            'door_table': door_table,
        }
        return HttpResponse(template.render(context, request))


def get_filtered_data(request):
    selected_model = request.GET.get('selected_model')
    filtered_data = DoorBlock.objects.filter(model=selected_model).values('width', 'height')
    
    return JsonResponse(list(filtered_data), safe=False)


def set_table_cookies(request):
    door_table = request.GET.get('door_table')

    response = HttpResponse()
    door_table = quote(door_table)
    response.set_cookie('door_table', door_table)
    return response


def get_price(request):
    model_d = request.GET.get('model')
    width_d = request.GET.get('width')
    height_d = request.GET.get('height')
    data = DoorBlock.objects.filter(model=model_d, width=width_d, height=height_d).values('price')
    
    return JsonResponse(list(data), safe=False)