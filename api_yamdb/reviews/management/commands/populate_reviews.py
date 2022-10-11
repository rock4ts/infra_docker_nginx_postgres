import csv
import os
import string

import inflect
from django.apps import apps
from django.db.models import ForeignKey
from django.core.management.base import BaseCommand, CommandError



class Command(BaseCommand):
    help = 'Populates database with specified model data'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        model_name, type = os.path.splitext(os.path.basename(path))
        p = inflect.engine()
        check_plural = p.singular_noun(model_name)

        if not check_plural:
            model_name = string.capwords(model_name, '_').replace('_', '')
        else:
            model_name = check_plural
            model_name = string.capwords(model_name, '_').replace('_', '')

        try:
            model = apps.get_model('reviews', model_name)
        except LookupError as e:
            raise CommandError(f"{model_name} model does not exist")
        
        model_fields = [field.name for field in model._meta.fields]
        file_fields = []

        with open(path, 'rt') as file:
            reader = csv.reader(file, delimiter=',')
            file_fields = next(reader)

            for i in range(len(file_fields)):
                file_fields[i] = file_fields[i].lower()
                file_fields[i] = file_fields[i].replace(' ', '_')
                if not file_fields[i] in model_fields:
                    raise CommandError(
                        f"{model.__name__} model"
                        f" does not have {file_fields[i]} field"
                    )

            for row in reader:
                obj = model()
                for i, field in enumerate(row):
                    model_field = obj._meta.get_field(file_fields[i])
                    if isinstance(model_field, ForeignKey):
                        field = model_field.related_model.objects.get(
                            pk=int(field)
                        )
                        setattr(obj, file_fields[i], field)
                    else:
                        setattr(obj, file_fields[i], field)
                obj.save()