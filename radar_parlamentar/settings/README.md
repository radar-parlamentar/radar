Settings
====================

Baseado no wiki do DJANGO: https://code.djangoproject.com/wiki/SplitSettings

Ao rodar python manage.py runserver no ambiente de desenvolvimento, será usado as configurações settings/development.py.

Para python manage.py test vai usar settings/test.py.

No ambiente de produção é necessário exportar a variável de ambiente export DJANGO_SETTINGS_MODULE='settings.production'.

