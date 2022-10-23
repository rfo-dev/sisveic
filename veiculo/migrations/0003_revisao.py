# Generated by Django 4.0.6 on 2022-07-21 12:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('veiculo', '0002_remove_usuario_nome'),
    ]

    operations = [
        migrations.CreateModel(
            name='Revisao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('KM', models.IntegerField(default=0)),
                ('Data', models.DateField()),
                ('veiculo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='veiculo.veiculo')),
            ],
        ),
    ]
