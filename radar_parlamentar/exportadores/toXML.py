import os,sys
import django.db.models
from environment import * 

writer = XMLWriter(pretty=False)
writer.open("djangoexport")
models = django.db.models.get_models()
for model in models:
    # model._meta.object_name holds the name of the model
    writer.open(model._meta.object_name + "s")
    for item in model.objects.all():
        writer.open(model._meta.object_name)
        for field in item._meta.fields:
            writer.open(field.name)
            value = getattr(item, field.name)
            if value != None:
                if isinstance(value, django.db.models.base.Model):
                    # This field is a foreign key, so save the primary key
                    # of the referring object
                    pk_name = value._meta.pk.name
                    pk_value = getattr(value, pk_name)
                    writer.content(pk_value)
                else:
                    writer.content(value)
            writer.close()
        writer.close()
    writer.close()
writer.close()
writer.save("export.xml")