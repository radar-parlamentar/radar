from django.db import (connections,DEFAULT_DB_ALIAS)
from django.core.management import call_command

def flush_db(cls):
    if getattr(cls,'multi_db',False):
        databases = connections
    else:
        databases = [DEFAULT_DB_ALIAS]
    for db_name in databases:
        call_command('flush',verbosity=0, interactive=False,database=db_name)
