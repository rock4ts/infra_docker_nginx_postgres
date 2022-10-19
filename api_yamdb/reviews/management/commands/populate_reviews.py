'''
Command to populate database with csv file data.

Script accepts file address, performs a check-up on file name,
automatically fetches relevant model by its name
and populates projects database with csv file data.

For script execution in the command line type:

python3 manage.py populate_reviews --path <path_name>

* <path_name> should end with csv file name
'''
import csv
import os
import string

import inflect
from django.apps import apps
from django.core.management.base import BaseCommand, CommandError
from django.db.models import ForeignKey


class Command(BaseCommand):
    help = "Populates database with specified model data"

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        model_name, type = os.path.splitext(os.path.basename(path))
        p = inflect.engine()
        to_singular = p.singular_noun(model_name)

        if not to_singular:
            model_name = string.capwords(model_name, '_').replace('_', '')
        else:
            model_name = string.capwords(to_singular, '_').replace('_', '')

        try:
            Model = apps.get_model('reviews', model_name)
        except LookupError:
            raise CommandError(f"{model_name} model does not exist")

        model_fields = [field.name for field in Model._meta.fields]
        file_fields = []

        with open(path, 'rt') as file:
            reader = csv.reader(file, delimiter=',')
            file_fields = next(reader)

            for i in range(len(file_fields)):
                file_fields[i] = file_fields[i].lower()
                file_fields[i] = file_fields[i].replace(' ', '_')
                file_fields[i] = file_fields[i].replace('_id', '')
                if not file_fields[i] in model_fields:
                    raise CommandError(
                        f"{Model.__name__} model"
                        f" does not have {file_fields[i]} field"
                    )

            for row in reader:
                obj = Model()
                for i, field_value in enumerate(row):
                    model_field = obj._meta.get_field(file_fields[i])
                    if isinstance(model_field, ForeignKey):
                        field_value = model_field.related_model.objects.get(
                            pk=int(field_value)
                        )
                        setattr(obj, file_fields[i], field_value)
                    else:
                        setattr(obj, file_fields[i], field_value)
                obj.save()
