from distutils.command.upload import upload
from email.policy import default
from pickle import FALSE
from turtle import title
import django
from django.db import models
from django.utils import timezone
from django.conf import settings

class Profile(models.Model):
    title = models.CharField('タイトル', max_length=100, null=True, blank=True)
    subtitle = models.CharField('サブタイトル', max_length=100, null=True, blank=True)
    name = models.CharField('名前', max_length=100)
    explanation1 = models.TextField('解説1')
    explanation2 = models.TextField('解説2',null=True,blank=True)
    explanation3 = models.TextField('解説3',null=True,blank=True)
    topimage1 = models.ImageField(upload_to='images', verbose_name='トップ画像1',null = True, blank=True)
    topimage2 = models.ImageField(upload_to='images', verbose_name='トップ画像2',null = True, blank=True)
    def __str__(self):
        return self.title

class Post(models.Model):
    name = models.CharField("名前",max_length=30,null=True)
    receiver = models.CharField("受取人",max_length=30,null=True)
    key = models.CharField("シークレットパス",max_length=200)
    message = models.TextField("本文")
    address = models.CharField("アドレス",max_length=200,null=True)
    image = models.ImageField(upload_to='images',verbose_name='QR画像',null=True)
    created_at = models.DateTimeField("作成日",default=timezone.now)
    updated_at = models.DateTimeField("閲覧日",null=True)
    count = models.IntegerField("カウント",default=0)

    def __str__(self):
        return self.name