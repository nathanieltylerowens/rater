# Generated by Django 3.1.4 on 2021-01-26 02:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('raterapi', '0002_auto_20210125_2329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviews',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', related_query_name='review', to='raterapi.game'),
        ),
        migrations.AlterField(
            model_name='reviews',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', related_query_name='review', to='raterapi.player'),
        ),
    ]
