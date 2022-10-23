# url - view - template
from django.urls import path, reverse_lazy
from .views import  criarviagem, homepage, veiculo,pesquisaveiculo,editarperfil,perfilusuario,finalizarviagem,addviagem,createReport,reportveiculo
from django.contrib.auth import views as auth_view
from django.urls import path
from . import views


app_name = 'veiculo'

urlpatterns = [
    path('', homepage.as_view(), name='homepage'),
    path('veiculo/<int:pk>', veiculo.as_view(), name='homeveiculo'),
    path('login/',auth_view.LoginView.as_view(template_name ='login.html' ) , name='login'),
    path('logout/',auth_view.LogoutView.as_view(template_name ='logout.html' ) , name='logout'),
    path('pesquisa/',pesquisaveiculo.as_view() , name='pesquisaveiculo'),
    path('editarperfil/<int:pk>',editarperfil.as_view(), name='editarperfil'),
    path('criarviagem/',views.criarviagem , name='criarviagem'),
    path('createreport/<int:id>', views.createReport, name='createreport'),
    path('reportveiculo/<int:id>', views.reportveiculo, name='reportveiculo'),
    path('finalizarviagem/<int:id>',views.finalizarviagem, name='finalizarviagem'),
    path('mudarsenha/<int:pk>',auth_view.PasswordChangeView.as_view(template_name='editarperfil.html',
    success_url=reverse_lazy('veiculo:homepage')), name='mudarsenha'),
    path('perfilusuario/', perfilusuario.as_view(), name='perfilusuario'),
]



