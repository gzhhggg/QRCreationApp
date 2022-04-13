from django.dispatch import receiver
from django.views.generic import View
from django.shortcuts import render,redirect
from requests import request
from urllib.parse import urljoin
from .models import Post , Profile
from .forms import PostForm 
import qrcode
import os
from django.conf import settings
import random
import string
import datetime
from django.utils import timezone
from django.core.mail import BadHeaderError, EmailMessage
from django.http import HttpResponse
import textwrap

class IndexView(View):
    def get(self, request, *args, **kwargs):
        profile_data = Profile.objects.all()
        if profile_data.exists():
            profile_data = profile_data.order_by("-id")[0]
        return render(request, 'app/index.html', {
            'profile_data': profile_data,
        })

class InputView(View):
    def get(self,request,*args,**kwargs):
        form = PostForm(request.POST or None)
        return render(request,'app/input.html',{
            'form':form,
        })
    def post(self,request,*args,**kwargs):
        form = PostForm(request.POST or None)
        key = (''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(30)))
        baseurl = request._current_scheme_host
        # baseurl = request.build_absolute_uri()
        relativeurl = 'other/' + key
        url = urljoin(baseurl,relativeurl)
        img = qrcode.make(url)
        img_path = settings.MEDIA_ROOT + "/images/" + key + ".jpg"
        img.save(img_path)
        if form.is_valid():
            name = form.cleaned_data['name']
            receiver = form.cleaned_data['receiver']
            email = form.cleaned_data['address']
            message = form.cleaned_data['message']
            
            post_data = Post()
            post_data.name = name
            post_data.key = key
            post_data.receiver = receiver
            post_data.address = email
            post_data.message = message
            post_data.image = img_path
            post_data.save()

            subject = 'QR作成連絡'
            content = textwrap.dedent('''
                ※このメールはシステムからの自動返信です。

                {name} 様
                QRを作成しました。
                作成されたQRは{name}様しか知りません。
                送り相手に送信してください。
                QRが開かれたときに通知が来ます。
                --------------------
                ■お名前
                {name}

                ■メールアドレス
                {email}

                ■メッセージ
                {message}
                --------------------
                ''').format(
                    name=name,
                    email=email,
                    message=message
                )

            to_list = [email]
            bcc_list = [settings.EMAIL_HOST_USER]

            try:
                message = EmailMessage(subject=subject, body=content, to=to_list, bcc=bcc_list)
                message.send()
            except BadHeaderError:
                return HttpResponse("無効なヘッダが検出されました。")

            return redirect('complite',post_data.key)

        return render(request,'app/input.html',{
            'form':form
        })

class CompliteView(View):
    def get(self,request,*args,**kwargs):
        post_data = Post.objects.get(key=self.kwargs['key'])
        return render(request,'app/complite.html',{
            'post_data':post_data
        })

class OtherView(View):
    def get(self,request,*args,**kwargs):
        post_data = Post.objects.get(key=self.kwargs['key'])
        post_data.count = post_data.count + 1
        post_data.save()
        if post_data.count > 5:
            os.remove(str(post_data.image))
            post_data.delete()
            return redirect('delete')
        now = now = timezone.now()
        elapsed_second = now - post_data.created_at
        def get_time(sec):
            td = datetime.timedelta(seconds=sec)
            m, s = divmod(td.seconds, 60)
            h, m = divmod(m, 60)
            elapsed_time = str(td.days)+'日'+str(h)+'時'+str(m)+'分'+str(s)+'秒'
            return elapsed_time
        elapsed_time = get_time(elapsed_second.seconds)

        name = post_data.name
        email = post_data.address
        subject = 'QR読み込み連絡'
        content = textwrap.dedent('''
            ※このメールはシステムからの自動返信です。

            {name} 様

            {name}様がQRコードを読み込みアクセスされました
            読み込むまでの時間；{elapsed_time}

            称賛の言葉をかけてあげてください!!

            アプリURL()
            --------------------
            ■お名前
            {name}

            ■メールアドレス
            {email}
            --------------------
            ''').format(
                name=name,
                elapsed_time=elapsed_time,
                email=email,
            )

        to_list = [email]
        bcc_list = [settings.EMAIL_HOST_USER]

        try:
            message = EmailMessage(subject=subject, body=content, to=to_list, bcc=bcc_list)
            message.send()
        except BadHeaderError:
            return HttpResponse("無効なヘッダが検出されました。")

        return render(request,'app/other.html',{
            'post_data':post_data,
            'elapsed_time':elapsed_time
        })

class DeleteView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'app/delete.html')

class DescriptionView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'app/description.html')
