from django.contrib import admin
from django.urls import path
from agro_site import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',             views.home,          name='home'),
    path('login/',       views.login_view,     name='login'),
    path('register/',    views.register_view,  name='register'),
    path('logout/',      views.logout_view,    name='logout'),
    path('crops/',       views.crops,          name='crops'),
    path('crops/<int:pk>/', views.crop_detail, name='crop_detail'),
    path('fertilizer/',  views.fertilizer,     name='fertilizer'),
    path('pesticide/',   views.pesticide,      name='pesticide'),
    path('marketplace/', views.marketplace,    name='marketplace'),
    path('crop-doc/',    views.crop_doc,       name='crop_doc'),
    path('mandi/',       views.mandi,          name='mandi'),
    path('weather/',     views.weather,        name='weather'),
    path('loan/',        views.loan,           name='loan'),
    path('diary/',       views.diary,          name='diary'),
    path('learn/',       views.learn,          name='learn'),
    path('soil/',        views.soil,           name='soil'),
    path('rent/',        views.rent,           name='rent'),
]
