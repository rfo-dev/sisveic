import datetime
import pytz
from gc import get_objects
from urllib import request, response
from reportlab.pdfgen import canvas
from webbrowser import get
from django.shortcuts import render, reverse,redirect
from django import forms
from .models import Usuario, Veiculo, Viagem,Revisao
from .forms import CriarViagemForm,FinalizarViagemForm
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView,CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib import messages
from reportlab.lib.pagesizes import letter, A4,landscape


    
class homepage(LoginRequiredMixin,ListView):
    template_name = "homepage.html"
    model = Veiculo  
    
class teste(LoginRequiredMixin,ListView):
    template_name = "teste.html"
    model = Veiculo  
    

class veiculo(LoginRequiredMixin,DetailView):
    template_name = "veiculo.html"
    model = Veiculo


class perfilusuario(LoginRequiredMixin,ListView):
    template_name = "perfilusuario.html"
    model = Usuario

class pesquisaveiculo(ListView):
    template_name = "pesquisa.html"
    model = Veiculo
    # filtrando a lista 
    def get_queryset(self):
        termo_pesquisa = self.request.GET.get('query')
        if termo_pesquisa:
            object_list = Veiculo.objects.filter(modelo__contains=termo_pesquisa)
            return object_list
        else: 
            return None  


class editarperfil(LoginRequiredMixin, UpdateView):
    template_name = "editarperfil.html"
    model = Usuario
    fields = ['first_name', 'last_name', 'email']

    def get_success_url(self):
        return reverse('veiculo:homepage')


@login_required
def criarviagem(request):
    if request.method == "POST":
        form = CriarViagemForm(request.POST)
        if form.is_valid():
            ViagemF = form.save(commit=False)
            ViagemF.motorista = request.user
            ViagemF.status = 'PENDENTE'
            ViagemF.save()
            post = get_object_or_404(Viagem, pk=ViagemF.id)
            post2 = get_object_or_404(Veiculo,id=post.veiculo_id)
            post2.status = 'OCUPADO'
            ViagemF.KM_Inicial = post2.kilometragem
            ViagemF.save()
            post2.save()

            messages.success(request,"Cadastrado com sucesso!")
            return render (request, 'homepage.html')
    else:
        form = CriarViagemForm()    
        carro = None

    return render(request,"criarviagem.html",{'form':form, 'carro': carro})


@login_required
def addviagem(request):
    if request.method == "POST":
        form = CriarViagemForm(request.POST)
        if form.is_valid():
            ViagemF = form.save(commit=False)
            ViagemF.motorista = request.user
            ViagemF.status = 'PENDENTE'
            ViagemF.save()
            post = get_object_or_404(Viagem, pk=ViagemF.id)
            post2 = get_object_or_404(Veiculo,id=post.veiculo_id)
            post2.status = 'OCUPADO'
            ViagemF.KM_Inicial = post2.kilometragem
            ViagemF.save()
            post2.save()

            messages.success(request,"Cadastrado com sucesso!")
            return render (request, 'addviagem.html')
    else:
        form = CriarViagemForm()    
        carro = None

    return render(request,"addviagem.html",{'form':form, 'carro': carro})


@login_required
def finalizarviagem(request,id):
    post = get_object_or_404(Viagem, pk=id)
    post2 = get_object_or_404(Veiculo,id=post.veiculo_id)
    form = FinalizarViagemForm (instance=post)
    if request.method == "POST":
        form = FinalizarViagemForm (request.POST,request.FILES,instance=post)
        if (form.is_valid()):
            post = form.save(commit=False)
            post.motorista = request.user

            if post.KM_Final < post2.kilometragem:
                messages.error(request,"KM final menor KM atual do veículo")
                return render (request, 'finalizarviagem.html',{'form':form, 'post' : post})

            elif post.KM_Final < post.KM_Inicial:
                messages.error(request,"KM final menor que KM inicial!")
                return render (request, 'finalizarviagem.html',{'form':form, 'post' : post})    

            else:
                post2.kilometragem = post.KM_Final
                post2.status = 'PENDENTE'
                post.status = 'FINALIZADA'
                post2.save()
                post.save()
                messages.success(request,"Finalizado com sucesso!")
                return redirect ('veiculo:perfilusuario')
        else:
            return render(request,"finalizarviagem.html",{'form':form, 'post' : post})
            #form = FinalizarViagemForm()    
    elif(request.method == 'GET'):

        return render(request,"finalizarviagem.html",{'form':form, 'post' : post})


@login_required
def createReport(request,id):
    
    response = HttpResponse()
    response['Content-Disposition'] = 'attachment; filename=filename.pdf'

    #p = canvas.Canvas(response,landscape(A4))
    p = canvas.Canvas(response)
   
    p.setFont("Helvetica-Bold", 10)

    dataAtual = datetime.datetime.now()
    dataAtual = dataAtual.strftime(("%d/%m/%Y - %H:%M:%S"))
    carro = get_object_or_404(Veiculo, pk=id)
    carro = (carro.modelo + "-" + carro.placa).upper()
    #p.line(480,747,580,747)
    p.drawImage('static/images/logo.png',20, 775,width=100, height=50)
    p.drawString(13, 770, 102*"_")
    p.drawString(470, 785, dataAtual)
    p.drawString(180, 730, f'RELATÓRIO DE VIAGENS DE {carro}')
    for i in range(809):
        p.drawString(580, 9+i, "|")
        p.drawString(10, 9+i, "|")

    for i in range(568):
        p.drawString(10+i, 10, "_")
        p.drawString(10+i, 825, "_")

    lista_viagens = Viagem.objects.all().order_by('-Data_Hora_Inicio')
    lista_viagens_final = []
    for viagem in lista_viagens:
        if viagem.veiculo_id == id:
            
            lista_viagens_final.append(viagem)
            
    # Cabeçalho
    p.drawString(15, 700, "Motorista")
    p.drawString(70, 700, 'Dt./Hr. Início')
    p.drawString(160, 700, 'Dt./Hr. Fim')
    p.drawString(250, 700, 'Origem')
    p.drawString(370, 700, 'Destino')
    p.drawString(480, 700, 'KM Inicial')
    p.drawString(535, 700, 'KM Final')

    p.setFont("Helvetica", 8)

    lin=690
    for trip in lista_viagens_final:
        
        lin-=15
        Data_Hora_Inicio = trip.Data_Hora_Inicio.strftime(("%d/%m/%Y - %H:%M:%S"))
        if trip.Data_Hora_Fim != None:
            Data_Hora_Fim = trip.Data_Hora_Fim.strftime(("%d/%m/%Y - %H:%M:%S"))
        else:
            Data_Hora_Fim = str(trip.Data_Hora_Fim)
            
        p.drawString(15, lin, str(trip.motorista))
        p.drawString(70, lin, Data_Hora_Inicio)
        p.drawString(160, lin, Data_Hora_Fim)
        p.drawString(250, lin, str(trip.origem))
        p.drawString(370, lin, str(trip.destino))
        p.drawString(480, lin, str(trip.KM_Inicial))
        p.drawString(535, lin, str(trip.KM_Final))

    p.showPage()
    p.save()
    return response


@login_required
def reportveiculo(request,id):
    inicio = request.POST.get('inicio')
    inicio = inicio[:4]+'/'+inicio[5:7]+'/'+inicio[8:10]+' '+inicio[11:20] + ':00'
    datahorainicio = datetime.datetime.strptime(inicio, "%Y/%m/%d %H:%M:%S")
    datahorainicio = datahorainicio.replace(tzinfo=pytz.UTC)
    fim = request.POST.get('fim')
    fim = fim[:4]+'/'+fim[5:7]+'/'+fim[8:10]+' '+fim[11:20] + ':00'
    datahorafim = datetime.datetime.strptime(fim, "%Y/%m/%d %H:%M:%S")
    datahorafim = datahorafim.replace(tzinfo=pytz.UTC)


    if datahorafim <= datahorainicio:
        messages.error(request,"Data final menor que inicial.")
        return HttpResponseRedirect('/veiculo/'+str(id))

    response = HttpResponse()
    response['Content-Disposition'] = 'attachment; filename=filename.pdf'

    #p = canvas.Canvas(response,landscape(A4))
    p = canvas.Canvas(response)
   
    p.setFont("Helvetica-Bold", 10)

    dataAtual = datetime.datetime.now()
    dataAtual = dataAtual.strftime(("%d/%m/%Y - %H:%M:%S"))
    carro = get_object_or_404(Veiculo, pk=id)
    carro = (carro.modelo + "-" + carro.placa).upper()
    #p.line(480,747,580,747)
    p.drawImage('static/images/logo.png',20, 775,width=100, height=50)
    p.drawString(13, 770, 102*"_")
    p.drawString(470, 785, dataAtual)
    p.drawString(180, 730, f'RELATÓRIO DE VIAGENS DE {carro}')
    for i in range(809):
        p.drawString(580, 9+i, "|")
        p.drawString(10, 9+i, "|")

    for i in range(568):
        p.drawString(10+i, 10, "_")
        p.drawString(10+i, 825, "_")

    lista_viagens = Viagem.objects.all().order_by('-Data_Hora_Inicio')
    lista_viagens_final = []
    for viagem in lista_viagens:
        if viagem.veiculo_id == id:
            if viagem.Data_Hora_Inicio >= datahorainicio and viagem.Data_Hora_Inicio <= datahorafim:
                lista_viagens_final.append(viagem)


    if not lista_viagens_final:
        messages.warning(request,"Sem viagens nesse periodo!")
        return HttpResponseRedirect('/veiculo/'+str(id))

    # Cabeçalho
    p.drawString(15, 700, "Motorista")
    p.drawString(70, 700, 'Dt./Hr. Início')
    p.drawString(160, 700, 'Dt./Hr. Fim')
    p.drawString(250, 700, 'Origem')
    p.drawString(370, 700, 'Destino')
    p.drawString(480, 700, 'KM Inicial')
    p.drawString(535, 700, 'KM Final')

    p.setFont("Helvetica", 8)

    lin=690
    for trip in lista_viagens_final:
        lin-=15
        Data_Hora_Inicio = trip.Data_Hora_Inicio.strftime(("%d/%m/%Y - %H:%M:%S"))
        if trip.Data_Hora_Fim != None:
            Data_Hora_Fim = trip.Data_Hora_Fim.strftime(("%d/%m/%Y - %H:%M:%S"))
        else:
            Data_Hora_Fim = str(trip.Data_Hora_Fim)
            
        p.drawString(15, lin, str(trip.motorista))
        p.drawString(70, lin, Data_Hora_Inicio)
        p.drawString(160, lin, Data_Hora_Fim)
        p.drawString(250, lin, str(trip.origem))
        p.drawString(370, lin, str(trip.destino))
        p.drawString(480, lin, str(trip.KM_Inicial))
        p.drawString(535, lin, str(trip.KM_Final))

    p.showPage()
    p.save()
    return response