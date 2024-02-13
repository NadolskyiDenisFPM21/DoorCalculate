from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
from django.conf import settings
from .models import DoorBlock, Frame, Table

from urllib.parse import quote, unquote
from .document_gen import excel, pdf
from ast import literal_eval

from datetime import datetime
from random import randint

from io import BytesIO

from xhtml2pdf import pisa, default
from xhtml2pdf.default import DEFAULT_CSS
from xhtml2pdf.files import pisaFileObject






def index(request):
    door_block_list = DoorBlock.objects.all()
    template = loader.get_template('polls/index.html')
    id: int
    try:
        id = request.COOKIES['id']
    except:
        return new_order(request=request)
    obj = Table.objects.filter(id=id).last()
    context = {
        'order_id': None,
        'door_block_list': door_block_list,
        'html': None
    }
    if obj:
        context['order_id'] = obj.id
        context['html'] = obj.html
        
    return HttpResponse(template.render(context, request))

def new_order(request):    
    new = Table.objects.create()
    id = new.id
    new.save()
    req = redirect('/')
    req.set_cookie('id', id)
    return req


def get_filtered_data(request):
    selected_model = request.GET.get('selected_model')
    selected_width = request.GET.get('selected_width')
    if selected_width is not None:
        filtered_data = list(DoorBlock.objects.filter(model=selected_model, width=selected_width).values('height'))
        frame_id_list = [id['frame'] for id in list(DoorBlock.objects.filter(model=selected_model, width=selected_width).values('frame'))]
    else:
        frame_id_list = [id['frame'] for id in list(DoorBlock.objects.filter(model=selected_model).values('frame'))]
        frames = [list(Frame.objects.filter(id=id).values('model'))[0]['model'] for id in frame_id_list]
        filtered_data = list(DoorBlock.objects.filter(model=selected_model).values('width', 'height'))
    
    frames = [list(Frame.objects.filter(id=id).values('model'))[0]['model'] for id in frame_id_list]
    for i in range(len(frames)):
        filtered_data[i]['frame'] = frames[i]
    
    return JsonResponse(filtered_data, safe=False)

def get_door_info(request):
    model_d = request.GET.get('model')
    width_d = request.GET.get('width')
    height_d = request.GET.get('height')
    frame_model = request.GET.get('frame')
    frame_id = Frame.objects.get(model=frame_model)
    data = DoorBlock.objects.filter(model=model_d, width=width_d, height=height_d, frame=frame_id).values('price', 'al_banding_canvas', 'profile_frame_color', 'seal_color', 'is_primed')
    
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
    id = request.COOKIES['id']
    table = Table.objects.get(id=id)
    html = table.html.replace('<th class="cell remove" rowspan="3">Удалить</th>', '')
    html = html.replace('<td rowspan="2"><button type="button" class="remove-button">Удалить дверь</button></td>', '')
    with open('polls/document_gen/to_excel.html', 'w', encoding='utf-8') as file:
        file.write(html)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=specification-{table.id}-{datetime.now().strftime("%y-%m-%d %H-%M-%S")}.xlsx'

    file = excel.create('')
    response.write(file)
    
    return response


def create_pdf_specification(request):
   
    html = request.GET.get('html')
    context_temp = {
        'html': html
    }
    template = loader.get_template('polls/to_pdf.html')
    html = template.render(context_temp)

    default.DEFAULT_CSS = DEFAULT_CSS.replace("background-color: transparent;", "", 1)
    # patch temporary file resolution when loading fonts
    pisaFileObject.getNamedFile = lambda self: self.uri
    with open('res.pdf', 'wb') as file:
        pdf2 = pisa.pisaDocument(BytesIO(html.encode("utf-8")), file)
    with BytesIO() as result:
        pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result, encoding="utf-8")
        if pdf.err:
            return HttpResponse("Invalid PDF", status_code=400, content_type='text/plain')
        response = HttpResponse(result.getvalue(), content_type='application/pdf; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename=specification-{datetime.now().strftime("%y-%m-%d %H-%M-%S")}.pdf'
                
        return response
    
@csrf_exempt
def set_table(request):
    html = request.POST.get('html', '')
    id = request.COOKIES['id']
    
    new = Table.objects.get(id=id)
    if not new:
        new = Table.objects.create()
        new.id = id
    new.html = html
    new.save()
    
    return JsonResponse(data='', safe=False)




def order_list(request):
    template = loader.get_template('polls/order_list.html')
    order_list = Table.objects.all()
    context = {
        'order_list': order_list
    }
    return HttpResponse(template.render(context=context, request=request))
    