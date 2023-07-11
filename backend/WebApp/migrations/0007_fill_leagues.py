# Generated by Django 3.2.6 on 2022-07-29 14:11

from django.db import migrations
from django.core.exceptions import ObjectDoesNotExist
import json

def insert_leagues(apps, schema_editor):
  League = apps.get_model('WebApp', 'League')

  f = open('data/leagues.json')
  data = json.load(f)

  for key, values in data.items():
    try:
      league = League.objects.get(name = key)
    except ObjectDoesNotExist:
      league = League(name = key)
      league.save()

class Migration(migrations.Migration):

    dependencies = [
        ('WebApp', '0006_fill_players'),
    ]

    operations = [
      migrations.RunPython(insert_leagues)
    ]
