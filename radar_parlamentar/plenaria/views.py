# -*- coding: utf-8 -*-

from modelagem import models
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from modelagem import utils
from . import serializer


def plenaria(request, nome_curto_casa_legislativa=None, identificador_proposicao=None):
    """identificador_proposicao: 'PL-123-2015'"""

    casas_legislativas = []
    for casa in models.CasaLegislativa.objects.all():
        #TODO: Remover após resolução da issue #377
        #       ( https://github.com/radar-parlamentar/radar/issues/377 )
        if casa.nome_curto != "cdep":
            casas_legislativas.append((casa.nome_curto, casa.nome))

    #TODO: Aqui precisa de uma verificação para quando não houver nenhuma casa.

    proposicoes = []
    if nome_curto_casa_legislativa is None:
        nome_curto_casa_legislativa = 'cmsp'
    if nome_curto_casa_legislativa:
        casa_legislativa = get_object_or_404(
            models.CasaLegislativa,
            nome_curto=nome_curto_casa_legislativa
        )
        proposicoes = [
            (identificador(prop), prop.nome())
            for prop in models.Proposicao.objects.filter(
                casa_legislativa__nome_curto=nome_curto_casa_legislativa
            )
        ]
    else:
        casa_legislativa = None

    return render_to_response(
        'plenaria.html',
        {
            'identificador_proposicao': identificador_proposicao,
            'casa_legislativa': casa_legislativa,
            'casas_legislativas': casas_legislativas,
            'proposicoes': proposicoes,
        },
        context_instance=RequestContext(request)
    )


def identificador(prop):
    return '-'.join([prop.sigla, prop.numero, prop.ano])


def json_proposicao(request, nome_curto_casa_legislativa, identificador_proposicao=None):
    """Retorna o JSON com os dados de todas as votações de uma proposição.
        identificador_proposicao: 'PL-123-2015'
    """
    sigla_proposicao, numero_proposicao, ano_proposicao = identificador_proposicao.split('-')
# comentado enquanto não se resolve #388
#    proposicao = get_object_or_404(
#        models.Proposicao, casa_legislativa__nome_curto=nome_curto_casa_legislativa,
#        sigla=sigla_proposicao, numero=numero_proposicao, ano=ano_proposicao)
    proposicoes = models.Proposicao.objects.filter(casa_legislativa__nome_curto=nome_curto_casa_legislativa,
        sigla=sigla_proposicao, numero=numero_proposicao, ano=ano_proposicao)
    if proposicoes:
        proposicao = proposicoes[0]
    else:
        raise Http404
    proposicao_serializer = serializer.ProposicaoSerializer()
    dados = proposicao_serializer.get_json_proposicao(proposicao)
    return HttpResponse(dados, mimetype='application/json')

