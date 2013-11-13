Settings
====================

Em ambiente de desenvolvimento:
Criar development.py baseado em development.py.template.

Em ambiente de produção:
Criar production.py baseado em production.py.template.

Ao rodar python manage.py runserver no ambiente de desenvolvimento, será usado as configurações settings/development.py.

Para python manage.py test vai usar settings/test.py.

No ambiente de produção é necessário exportar a variável de ambiente export DJANGO_SETTINGS_MODULE='settings.production'.
Para isso basta executar o script is_prod.sh.

Referência do DJANGO: https://code.djangoproject.com/wiki/SplitSettings


