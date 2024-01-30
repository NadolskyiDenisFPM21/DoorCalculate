from django.http import HttpResponse, JsonResponse
from django.template import loader
from .models import DoorBlock, Frame

from urllib.parse import quote, unquote
from .document_gen import excel, pdf
from ast import literal_eval

from datetime import datetime


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
            data = literal_eval(unquote(request.COOKIES['door_table']))
    else:
        return JsonResponse(data=f"Таблица пустая!", status=500, safe=False)
    
    data_dict = {
        'Модель': [],
        'Открывание':[],
        'Ширина полотна мм': [],
        'Высота полотна мм': [],
        'Минимальная ширина проема мм':[],
        'Минимальная высота проема мм':[],
        'Тип короба':[],
        'Алюминиевый обвяз полотна':[],
        'Цвет покраски профиля и короба':[],
        'Цвет уплотнителя':[],
        'Ширина короба мм':[],
        'Высота короба мм':[],
        'Отверствия ручка':[],
        'Петли':[],
        'Количество':[],
        'Цена':[],
        'Всего':[],
    }
    for row in data:
        for i, key in enumerate(data_dict.keys()):
            data_dict[key].append(row[i])
    
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=specification-{datetime.now().strftime("%y-%m-%d %H-%M-%S")}.xlsx'

    file = excel.create(data_dict)
    response.write(file)
    
    return response

def create_pdf_specification(request):
    if 'door_table' in request.COOKIES.keys():
            data = literal_eval(unquote(request.COOKIES['door_table']))
    else:
        return JsonResponse(data=f"Таблица пустая!", status=500, safe=False)
    
    data_dict = {
        'Модель': [],
        'Открывание':[],
        'Ширина полотна мм': [],
        'Высота полотна мм': [],
        'Мин ширина проема мм':[],
        'Мин высота проема мм':[],
        'Тип короба':[],
        'Обвяз полотна':[],
        'Цвет профиля и короба':[],
        'Цвет уплотнителя':[],
        'Ширина короба мм':[],
        'Высота короба мм':[],
        'Отверствия ручка':[],
        'Петли':[],
        'Кол-во':[],
        'Цена':[],
        'Всего':[],
    }
    for row in data:
        for i, key in enumerate(data_dict.keys()):
            data_dict[key].append(row[i])
    
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=specification-{datetime.now().strftime("%y-%m-%d %H-%M-%S")}.pdf'

    file = pdf.create(data_dict)
    response.write(file)
    
    return response
    
    
def set_table_cookies(request):
    door_table = request.GET.get('door_table')

    response = HttpResponse()
    door_table = quote(door_table)
    response.set_cookie('door_table', door_table)
    return response

    