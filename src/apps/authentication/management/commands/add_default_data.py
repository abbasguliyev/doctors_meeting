from django.core.management.base import BaseCommand
from django.db.models import Count
from apps.authentication.selectors import disease_list, profession_list
from apps.authentication.models import Disease, Profession
from datetime import timedelta, datetime
from django.utils.timezone import utc
import json, os
  
def now():
    return datetime.utcnow().replace(tzinfo=utc)
  
  
class Command(BaseCommand):
    help = 'Add default data to database'
    
    def handle(self, *args, **kwargs):
        # Disease add
        with open(os.path.join('apps/authentication/management/commands/diseases.json'), 'r') as f:
            diseases = json.load(f)
            for disease in diseases:
                name = disease.get('name')
                disease_instance_count = disease_list().filter(name=name).count()
                if disease_instance_count == 0:
                    disease_instance = Disease.objects.create(name=name)
                    disease_instance.save()
        # Profession add
        with open(os.path.join('apps/authentication/management/commands/professions.json'), 'r') as f:
            professions = json.load(f)
            for profession in professions:
                name = profession.get('name')
                profession_instance_count = profession_list().filter(name=name).count()
                if profession_instance_count == 0:
                    profession_instance = Profession.objects.create(name=name)
                    profession_instance.save()
        
