from django.db import models
from core.__seedwork.domain.entities import Entity

print(Entity)

# Create your models here.
class CategoryModel(models.Model):
    name = models.CharField(max_length=255)
