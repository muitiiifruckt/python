# Generated by Django 5.0.1 on 2024-03-16 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChessGame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('white_player', models.CharField(max_length=100)),
                ('black_player', models.CharField(max_length=100)),
                ('event', models.CharField(blank=True, max_length=100, null=True)),
                ('site', models.CharField(blank=True, max_length=100, null=True)),
                ('date', models.DateField()),
                ('round', models.CharField(blank=True, max_length=10, null=True)),
                ('result', models.CharField(max_length=7)),
                ('pgn_text', models.TextField()),
            ],
        ),
    ]