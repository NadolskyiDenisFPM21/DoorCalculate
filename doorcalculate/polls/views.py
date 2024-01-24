from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader
from .models import DoorBlock, Frame

from urllib.parse import quote, unquote
from ..document_gen import excel


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
    frame_id_list = [id['frame'] for id in list(DoorBlock.objects.filter(model=selected_model).values('frame'))]
    frames = [list(Frame.objects.filter(id=id).values('model'))[0]['model'] for id in frame_id_list]
    filtered_data = list(DoorBlock.objects.filter(model=selected_model).values('width', 'height'))
    for i in range(len(frames)):
        filtered_data[i]['frame'] = frames[i]
    
    return JsonResponse(filtered_data, safe=False)


def set_table_cookies(request):
    door_table = request.GET.get('door_table')

    response = HttpResponse()
    door_table = quote(door_table)
    response.set_cookie('door_table', door_table)
    return response


def get_door_info(request):
    model_d = request.GET.get('model')
    width_d = request.GET.get('width')
    height_d = request.GET.get('height')
    frame_model = request.GET.get('frame')
    frame_id = Frame.objects.get(model=frame_model)
    data = DoorBlock.objects.filter(model=model_d, width=width_d, height=height_d, frame=frame_id).values('price', 'al_banding_canvas', 'profile_frame_color', 'seal_color')
    
    return JsonResponse(list(data), safe=False)


def get_dimensions_aperture(request):
    frame = Frame.objects.get(model=request.GET.get('frame'))
    width_door = int(request.GET.get('width_door'))
    height_door = int(request.GET.get('height_door'))
    width = 28 + frame.depth*2 + width_door
    height = 22 + frame.depth + height_door
    
    data = {
        'aperture_width': width,
        'aperture_height': height    
    }
    
    return JsonResponse(data, safe=False)

def get_dimensions_frame(request):
    frame = Frame.objects.get(model=request.GET.get('frame'))
    width_door = int(request.GET.get('width_door'))
    height_door = int(request.GET.get('height_door'))
    width = 8 + frame.depth*2 + width_door
    height = 12 + frame.depth + height_door
    
    data = {
        'frame_width': width,
        'frame_height': height    
    }
    
    return JsonResponse(data, safe=False)

def get_back_width(request):
    width = int(request.GET.get('width'))
    height = int(request.GET.get('height'))
    frame = Frame.objects.get(model=request.GET.get('frame'))
    back_width = width - 2*frame.width_back_indent
    back_height = height - frame.width_back_indent
    
    data = {
        'back_width': back_width,
        'back_height': back_height,
    }
    print(data)
    
    return JsonResponse(data=data, safe=False)


def create_excel_specification(request):
    if 'door_table' in request.COOKIES.keys():
            data = unquote(request.COOKIES['door_table'])
    else:
        return JsonResponse(data=f"Таблица пустая!", status=500)
    
    
    
    excel.create(data)
    
    
    