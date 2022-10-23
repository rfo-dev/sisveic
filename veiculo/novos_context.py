from ast import Break
from .models import Revisao, Veiculo,Viagem,Usuario


def lista_viagens_usuarios(request):
    lista_viagens_pendentes = []
    lista_viagens_finalizadas = []
    lista_viagens = Viagem.objects.all().order_by('-Data_Hora_Inicio')   
    for viagem in lista_viagens:
        if viagem.motorista == request.user and viagem.status == 'PENDENTE':
            lista_viagens_pendentes.append(viagem)

        if viagem.motorista == request.user and viagem.status == 'FINALIZADA':
            lista_viagens_finalizadas.append(viagem)

    return {"lista_viagens_finalizadas": lista_viagens_finalizadas[:5], "lista_viagens_pendentes":lista_viagens_pendentes[:5]}


def lista_veiculos_cadastrados(request):
    lista_carros = Veiculo.objects.all().order_by('data_criacao')    
    return {"lista_veiculos_cadastrados": lista_carros}


def lista_revisoes_realizadas(request):
    carros_revisoes = []
    lista_carros = Veiculo.objects.all().order_by('data_criacao')
    lista_revisoes = Revisao.objects.all().order_by('-Data')
    for carro in lista_carros:
        for revisao in lista_revisoes:
            if carro == revisao.veiculo:
                carros_revisoes.append(revisao)
                break         
    return {"lista_revisoes_realizadas": carros_revisoes}


def lista_viagens_realizadas(request):
    lista_viagens = Viagem.objects.all().order_by('-Data_Hora_Inicio')
    lista_viagens_final = []
    for viagem in lista_viagens:
        if viagem.status == 'PENDENTE':
            lista_viagens_final.append(viagem)          
    return {"lista_viagens_realizadas": lista_viagens_final}


def lista_proximas_revisoes(request):
    proximas_revisoes = {}
    lista_carros = Veiculo.objects.all().order_by('data_criacao')
    lista_revisoes = Revisao.objects.all().order_by('-Data')
    for carro in lista_carros:
        for revisao in lista_revisoes:
            if carro == revisao.veiculo:
                proximas_revisoes[carro.pk]=carro.KM_Revisao + revisao.KM
                break
    return {"lista_proximas_revisoes": proximas_revisoes}


