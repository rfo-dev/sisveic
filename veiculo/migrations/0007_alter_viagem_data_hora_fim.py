# Generated by Django 4.0.6 on 2022-07-24 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('veiculo', '0006_alter_viagem_destino'),
    ]

    operations = [
        migrations.AlterField(
            model_name='viagem',
            name='Data_Hora_Fim',
            field=models.DateTimeField(null=True),
        ),
    ]
