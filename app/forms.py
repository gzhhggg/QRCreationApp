from cProfile import label
from django import forms

class PostForm(forms.Form):
    name = forms.CharField(label='ニックネーム/名前',max_length=30)
    receiver = forms.CharField(label='送り相手の名前',max_length=30)
    message = forms.CharField(label='本文', widget=forms.Textarea())
    address = forms.EmailField(label='アドレス',max_length=100)