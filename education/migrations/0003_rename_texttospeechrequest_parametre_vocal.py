# Generated by Django 5.0.2 on 2024-11-19 11:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0002_texttospeechrequest_remove_contenu_parametre_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TextToSpeechRequest',
            new_name='Parametre_vocal',
        ),
    ]
