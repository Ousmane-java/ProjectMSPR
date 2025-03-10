# Generated by Django 5.1.5 on 2025-02-19 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sondes', '0006_remove_franchise_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='franchise',
            name='status',
            field=models.CharField(choices=[('connected', 'Connecté'), ('disconnected', 'Déconnecté')], default='connected', help_text='État actuel de la franchise', max_length=20),
        ),
        migrations.AlterField(
            model_name='franchise',
            name='last_modified',
            field=models.DateTimeField(blank=True, help_text="Dernière mise à jour de l'IP ou des ports", null=True),
        ),
    ]
