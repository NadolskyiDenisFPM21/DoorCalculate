from django.db import models
from django.utils import timezone

class Frame(models.Model):
    model = models.CharField(max_length=50)
    depth = models.IntegerField()
    opening_type = models.CharField(max_length=50)
    opening_type2 = models.CharField(max_length=50)
    width_back_indent = models.IntegerField()

    def __str__(self) -> str:
        return self.model


class DoorBlock(models.Model):
    model = models.CharField(max_length=50)
    width = models.IntegerField()
    height = models.IntegerField()
    frame = models.ForeignKey(Frame, on_delete=models.CASCADE)
    al_banding_canvas = models.BooleanField()
    profile_frame_color = models.CharField(max_length=50)
    seal_color = models.CharField(max_length=50)
    is_primed = models.CharField(max_length=50)
    price = models.IntegerField()

    def __str__(self) -> str:
        return self.model



class Table(models.Model):
    order_number = models.IntegerField()
    html = models.TextField()
    total = models.FloatField()
    sale = models.FloatField()
    total_with_sale = models.FloatField()
    delivery = models.FloatField()
    install = models.FloatField()
    poslugy = models.FloatField()
    measurements = models.FloatField()
    total_ex_vat = models.FloatField()
    prepayment = models.FloatField()
    remainder = models.FloatField()
    manager = models.CharField(max_length=50)
    manager_phone = models.CharField(max_length=15)
    date = models.DateField(default=timezone.now().strftime("%Y-%m-%d"))
    city = models.CharField(max_length=50)
    client = models.CharField(max_length=50)
    delivery_info = models.CharField(max_length=150)
    client_contact = models.CharField(max_length=100)
    client_email = models.EmailField(max_length=254)
    note = models.TextField()