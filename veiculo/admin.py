from django.contrib import admin
from .models import Veiculo, Viagem,Usuario,Revisao
from django.contrib.auth.admin import UserAdmin

campos = list(UserAdmin.fieldsets)
campos.append(
    ("Documentos Pessoais",{'fields':('CPF','CNH','categoria',)})
)

UserAdmin.fieldsets = tuple(campos)
# Register your models here.

admin.site.register(Veiculo)
admin.site.register(Viagem)
admin.site.register(Revisao)
admin.site.register(Usuario, UserAdmin)
