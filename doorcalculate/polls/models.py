from django.db import models



class Frame(models.Model):
    model = models.CharField(max_length=50)
    depth = models.IntegerField()
    width_back_indent = models.IntegerField()
    
    def __str__(self) -> str:
        return self.model


class DoorBlock(models.Model):
    model = models.CharField(max_length=50)
    width = models.IntegerField()
    height = models.IntegerField()
    article = models.IntegerField(unique=True, blank=True)
    opening_type = models.CharField(max_length=50)
    frame = models.ForeignKey(Frame, on_delete=models.CASCADE)
    al_banding_canvas = models.BooleanField()
    profile_frame_color = models.CharField(max_length=50)
    seal_color = models.CharField(max_length=50)
    is_primed = models.CharField(max_length=50)
    price = models.IntegerField()
    
    def __str__(self) -> str:
        return self.model
    
    

class Table(models.Model):
    csrf = models.CharField(max_length=100)
    html = models.TextField()
