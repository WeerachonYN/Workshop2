from django.db import models
from django.contrib.auth.models import User
import datetime


STATUS_CHOICE = (
    ('Wait', 'รอส่ง'),
    ('Success', 'ส่งแล้ว'),
    ('Cancel', 'ยกเลิก'),
)

class invoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='invoices',default=None,null=True)
    created_datetime = models.DateTimeField(auto_now=True)
    updated_datetime = models.DateTimeField(default=None,null=True)
    total = models.DecimalField(max_digits=7, decimal_places=2)
    status = models.CharField(choices=STATUS_CHOICE,default='Wait',max_length=100)
    
    def save(self, *args, **kwargs):
            self.updated_datetime = datetime.datetime.now()
            super().save(*args, **kwargs)

    def __str__(self):
            return self.user.username
