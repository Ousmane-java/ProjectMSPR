# Generated by Django 5.1.5 on 2025-01-22 08:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Franchise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Nom de la franchise', max_length=100, unique=True)),
                ('ip_address', models.GenericIPAddressField(help_text='Adresse IP de la franchise')),
                ('location', models.CharField(blank=True, help_text='Localisation de la franchise', max_length=255, null=True)),
                ('last_seen', models.DateTimeField(auto_now=True, help_text='Dernière activité enregistrée')),
                ('contact_person', models.CharField(blank=True, help_text='Personne à contacter', max_length=100, null=True)),
                ('contact_email', models.EmailField(blank=True, help_text='Email de contact', max_length=254, null=True)),
                ('contact_phone', models.CharField(blank=True, help_text='Téléphone de contact', max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ApplicationVersion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(help_text="Version de l'application déployée", max_length=50)),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Date de mise à jour')),
                ('franchise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='application_versions', to='sondes.franchise')),
            ],
        ),
        migrations.CreateModel(
            name='NetworkLatency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latency', models.FloatField(help_text='Latence moyenne (ms)')),
                ('timestamp', models.DateTimeField(auto_now_add=True, help_text='Date et heure de la mesure')),
                ('franchise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='latencies', to='sondes.franchise')),
            ],
        ),
        migrations.CreateModel(
            name='ScanReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scan_data', models.JSONField(help_text='Résultats du scan en format JSON (machines connectées, ports)')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date du scan')),
                ('franchise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scan_reports', to='sondes.franchise')),
            ],
        ),
        migrations.CreateModel(
            name='SondaStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('connected', 'Connecté'), ('disconnected', 'Déconnecté')], default='disconnected', help_text='Statut de la sonde', max_length=20)),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Dernière mise à jour du statut')),
                ('franchise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sonda_status', to='sondes.franchise')),
            ],
        ),
    ]
