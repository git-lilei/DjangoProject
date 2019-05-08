# Generated by Django 2.2 on 2019-05-08 09:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asset',
            name='admin',
        ),
        migrations.AddField(
            model_name='asset',
            name='admin1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='admin1', to='assets.User', verbose_name='资产管理员'),
        ),
    ]
