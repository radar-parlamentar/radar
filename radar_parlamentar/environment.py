import os
import sys
import django.db.models
sys.path.append(os.pardir)
os.environ["DJANGO_SETTINGS_MODULE"] = "settings"


class XMLWriter:

    """Helper class to write out an xml file"""

    def __init__(self, pretty=True):
        """Set pretty to True if you want an indented XML file"""
        self.output = ""
        self.stack = []
        self.pretty = pretty

    def open(self, tag):
        """Add an open tag"""
        self.stack.append(tag)
        if self.pretty:
            self.output += "  " * (len(self.stack) - 1)
        self.output += "<" + tag + ">"
        if self.pretty:
            self.output += "\n"

    def close(self):
        """Close the innermost tag"""
        if self.pretty:
            self.output += "\n" + "  " * (len(self.stack) - 1)
        tag = self.stack.pop()
        self.output += "</" + tag + ">"
        if self.pretty:
            self.output += "\n"

    def closeAll(self):
        """Close all open tags"""
        while len(self.stack) > 0:
            self.close()

    def content(self, text):
        """Add some content"""
        if self.pretty:
            self.output += "  " * len(self.stack)
        self.output += str(text)

    def save(self, filename):
        """Save the data to a file"""
        self.closeAll()
        fp = open(filename, "w")
        fp.write(self.output)
        fp.close()


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
            if value is not None:
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
