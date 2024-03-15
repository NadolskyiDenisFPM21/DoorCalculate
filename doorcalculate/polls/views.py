from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
from django.conf import settings
from django.utils import timezone

from . import excel
from .models import DoorBlock, Frame, Table

from urllib.parse import quote, unquote
from ast import literal_eval

from datetime import datetime
from random import randint

from io import BytesIO

from xhtml2pdf import pisa, default
from xhtml2pdf.default import DEFAULT_CSS
from xhtml2pdf.files import pisaFileObject

import os






def index(request):
    door_block_list = DoorBlock.objects.all().order_by('model')
    template = loader.get_template('polls/index.html')
    id: int
    try:
        id = request.COOKIES['id']
        obj = Table.objects.filter(id=id).last()
    except:
        return new_order(request=request)

    context = {
        'order_id': None,
        'door_block_list': door_block_list,
        'html': None,
        'date': timezone.now().strftime("%Y-%m-%d"),
        'table': None
    }
    if obj:
        context['order_id'] = obj.id
        context['html'] = obj.html
        context['table'] = obj


    return HttpResponse(template.render(context, request))

def new_order(request):
    new = Table.objects.create(html = '',
    order_number = 0,
    total = 0,
    sale = 0,
    total_with_sale = 0,
    delivery = 0,
    install = 0,
    measurements = 0,
    poslugy = 0,
    total_ex_vat = 0,
    prepayment = 0,
    remainder = 0)
    id = new.id

    new.save()
    req = redirect('/')
    req.set_cookie('id', id)
    return req


def get_filtered_data(request):
    selected_model = request.GET.get('selected_model')
    selected_frame = request.GET.get('selected_frame')
    if selected_frame != '':
        selected_frame = Frame.objects.get(model=selected_frame)
    selected_width = request.GET.get('selected_width')
    if selected_width != '':
        filtered_data = list(DoorBlock.objects.filter(model=selected_model, width=selected_width, frame=selected_frame).values('height'))
    elif selected_frame != '':
        filtered_data = list(DoorBlock.objects.filter(model=selected_model, frame=selected_frame).values('width'))
        for i in range(len(filtered_data)):
            filtered_data[i]['opening_type2'] = selected_frame.opening_type2.split(';')
    else:
        frame_id_list = [id['frame'] for id in list(DoorBlock.objects.filter(model=selected_model).values('frame'))]
        frames = [list(Frame.objects.filter(id=id).values('model'))[0]['model'] for id in frame_id_list]
        filtered_data = []

        for i in range(len(frames)):
            filtered_data.append({'frame': frames[i]})



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

def format_table(html):
    html = html.replace('<th class="cell remove" rowspan="3">Del</th>', '')
    html = html.replace('<td rowspan="2" class="remove-button">⮾</td>', '')
    return html


def create_excel_specification(request):
    id = request.COOKIES['id']
    table = Table.objects.get(id=id)
    html = Table.objects.get(id=id).html
    html = format_table(html)
    context_temp = {
        'html': html,
        'table': table,
        'prepayment_value': table.prepayment*table.total_ex_vat/100
    }
    template = loader.get_template('polls/to_excel.html')
    html = template.render(context_temp)
    with open(str(settings.BASE_DIR) + '\\polls\\to_excel.html', 'w', encoding='utf-8') as file:
        file.write(html)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=specification-{id}-{datetime.now().strftime("%y-%m-%d %H-%M-%S")}.xlsx'

    file = excel.create('\\polls\\to_excel.html')
    response.write(file)

    return response


def link_callback(uri, rel):
    # use short variable names
    sUrl = settings.STATIC_URL      # Typically /static/
    sRoot = settings.STATICFILES_DIRS[0]    # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL       # Typically /static/media/
    mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/
    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        path = uri

    pisaFileObject.getNamedFile = lambda self: path

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception('media URI must start with %s or %s but %s' % (sUrl, mUrl, path))
    return path


def create_pdf_specification(request):
    id = request.COOKIES['id']
    table = Table.objects.get(id=id)
    html = format_table(table.html)
    context_temp = {
        'html': html,
        'table': table,
        'prepayment_value': table.prepayment*table.total_ex_vat/100
    }
    template = loader.get_template('polls/to_pdf.html')
    html = template.render(context_temp)
    # return HttpResponse(template.render(context_temp, request))
    # pisaFileObject.getNamedFile = lambda self: self.uri

    with BytesIO() as result:
        pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result, encoding="utf-8", link_callback=link_callback)
        if pdf.err:
            return HttpResponse("Invalid PDF", status_code=400, content_type='text/plain')
        response = HttpResponse(result.getvalue(), content_type='application/pdf; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename=specification-{datetime.now().strftime("%y-%m-%d %H-%M-%S")}.pdf'

        return response



@csrf_exempt
def set_table(request):
    order_number = request.POST.get('order_number', '')
    html = request.POST.get('html', '')
    total = request.POST.get('total', '')
    sale = request.POST.get('sale', '')
    total_with_sale = request.POST.get('total_with_sale', '')
    delivery = request.POST.get('delivery', '')
    install = request.POST.get('install', '')
    measurements = request.POST.get('measurements', '')
    poslugy = request.POST.get('poslugy', '')
    total_ex_vat = request.POST.get('total_ex_vat', '')
    prepayment = request.POST.get('prepayment', '')
    remainder = request.POST.get('remainder', '')
    manager = request.POST.get('manager', '')
    manager_phone = request.POST.get('manager_phone', '')
    city = request.POST.get('city', '')
    client = request.POST.get('client', '')
    client_contact = request.POST.get('client_contact', '')
    delivery_info = request.POST.get('delivery_info', '')
    client_email = request.POST.get('client_email', '')
    note = request.POST.get('note', '')
    id = request.COOKIES['id']

    new = Table.objects.get(id=id)
    if not new:
        new = Table.objects.create()
        new.id = id
    new.html = html
    new.order_number = order_number
    new.total = total
    new.sale = sale
    new.total_with_sale = total_with_sale
    new.delivery = delivery
    new.install = install
    new.measurements = measurements
    new.poslugy = poslugy
    new.total_ex_vat = total_ex_vat
    new.prepayment = prepayment
    new.remainder = remainder
    new.manager = manager
    new.manager_phone = manager_phone
    new.city = city
    new.client = client
    new.client_contact = client_contact
    new.delivery_info = delivery_info
    new.client_email = client_email
    new.note = note
    new.save()

    return JsonResponse(data='', safe=False)




def order_list(request):
    template = loader.get_template('polls/order_list.html')
    order_list = Table.objects.all()
    context = {
        'order_list': order_list
    }
    return HttpResponse(template.render(context=context, request=request))

