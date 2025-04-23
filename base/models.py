from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_created_by', null=False, blank=False) # Hacer obligatorio el campo
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_updated_by', null=False, blank=False) # Hacer obligatorio el campo
    status = models.BooleanField(default=True, verbose_name='Estado', help_text='Estado del registro')
    class Meta:
        abstract = True