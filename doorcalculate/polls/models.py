from django.db import models

class DoorBlock(models.Model):
    model = models.CharField(max_length=50)
    width = models.IntegerField()
    height = models.IntegerField()
    article = models.IntegerField(unique=True, blank=True)
    opening_type = models.CharField(max_length=50)
    price = models.IntegerField()

    def __str__(self) -> str:
        return self.model
    
