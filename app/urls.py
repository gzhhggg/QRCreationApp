from django.urls import path
from app import views

urlpatterns = [
    path('',views.IndexView.as_view(),name='index'),
    path('input/',views.InputView.as_view(),name='input'),
    path('complite/<str:key>/',views.CompliteView.as_view(),name='complite'),
    path('other/<str:key>/',views.OtherView.as_view(),name='other'),
    path('delete/',views.DeleteView.as_view(),name='delete'),
    path('description/',views.DescriptionView.as_view(),name='description'),
]