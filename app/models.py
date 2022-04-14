from distutils.command.upload import upload
from email.policy import default
from pickle import FALSE
from turtle import title
import django
from django.db import models
from django.utils import timezone
from django.conf import settings

class Post(models.Model):
    name = models.CharField("名前",max_length=30,null=True)
    receiver = models.CharField("受取人",max_length=30,null=True)
    key = models.CharField("シークレットパス",max_length=200)
    message = models.TextField("本文")
    address = models.CharField("アドレス",max_length=200,null=True)
    image = models.ImageField(upload_to='images',verbose_name='QR画像',null=True)
    created_at = models.DateTimeField("作成日",default=timezone.now)
    updated_at = models.DateTimeField("閲覧日",null=True ,blank=True)
    count = models.IntegerField("カウント",default=0)

    def __str__(self):
        return self.name