from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import DateTimeField, DateTimeInput, ModelForm
from django.forms.widgets import DateTimeInput
from bootstrap_datepicker_plus.widgets import DatePickerInput, TimePickerInput, DateTimePickerInput, MonthPickerInput, YearPickerInput
from .models import Viagem

class DateInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class CriarViagemForm(forms.ModelForm):
    class Meta:
        model = Viagem
        
        fields = ['veiculo','origem','destino','Data_Hora_Inicio']
        widgets = {
            'Data_Hora_Inicio' : DateInput(),
            }

class FinalizarViagemForm(forms.ModelForm):
    class Meta:
        model = Viagem

        fields = ['destino','KM_Final','Data_Hora_Fim','fotos']
        widgets = {
            'Data_Hora_Fim': DateInput(),
            }


 
        #fields = '__all__'

    # origem = forms.CharField(label='origem', max_length=100)
    # destino = forms.CharField(label='destino', max_length=100)
    # destino2 = forms.CharField(label='destino2', max_length=100)
    # destino3 = forms.CharField(label='destino3', max_length=100)
    # KM_Inicial  = forms.FloatField(label='KMInicio')
    # KM_Final = forms.FloatField(label='KMFim')
    # Data_Hora_Inicio = forms.DateTimeField(label='DataInicio')
    # Data_Hora_Fim = forms.DateTimeField(label='DataFim')

    # class Meta:
    #     model = Viagem
    #     fields = ['origem','destino','destino2','destino3', 'KM_Inicial','KM_Final','Data_Hora_Inicio','Data_Hora_Fim']

