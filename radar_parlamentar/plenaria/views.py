# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from modelagem import models
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from . import serializer


def plenaria(request, nome_curto_casa_legislativa=None, id_proposicao=None):
    proposicoes = []
    if nome_curto_casa_legislativa:
        casa_legislativa = get_object_or_404(
            models.CasaLegislativa,
            nome_curto=nome_curto_casa_legislativa
        )
        proposicoes = [
            (prop.id, prop.nome())
            for prop in models.Proposicao.objects.filter(
                casa_legislativa__nome_curto=nome_curto_casa_legislativa
            )
        ]
    else:
        casa_legislativa = None
    return render_to_response(
        'plenaria.html',
        {
            'id_proposicao': id_proposicao,
            'casa_legislativa': casa_legislativa,
            'casas_legislativas': [('cmsp', 'Câmara Municipal de São Paulo')],
            'proposicoes': proposicoes,
        },
        context_instance=RequestContext(request)
    )


def json_proposicao(request, nome_curto_casa_legislativa, id_proposicao):
    """Retorna o JSON com os dados de todas as votações de uma proposição."""
    proposicao = get_object_or_404(
        models.Proposicao, id=id_proposicao)
    proposicao_serializer = serializer.ProposicaoSerializer()
    dados = proposicao_serializer.get_json_proposicao(proposicao)
    return HttpResponse(dados, mimetype='application/json')
