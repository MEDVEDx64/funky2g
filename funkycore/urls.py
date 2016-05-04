import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/', views.login_view, name='login'),
    url(r'^logout/', views.logout_view, name='logout'),
    url(r'^message/', views.message, name='message'),
    url(r'^transfer/', views.transfer_view, name='transfer'),
    url(r'^settings/', views.settings_view, name='transfer'),
    url(r'^buy/', views.buy, name='buy'),
]