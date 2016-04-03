# !/usr/bin/python
# coding=utf8

# Copyright (C) 2013, Arthur Del Esposte, David Carlos de Araujo Silva
#
# This file is part of Radar Parlamentar.
#
# Radar Parlamentar is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Radar Parlamentar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Radar Parlamentar.  If not, see <http://www.gnu.org/licenses/>.

from django.http import Http404, HttpResponse

import mimetypes
import os
MODULE_DIR = os.path.abspath(os.path.dirname(__file__))


def download_dados(request, dado_solicitado):

    arquivo = os.path.join(MODULE_DIR, 'dados/' + dado_solicitado + '.xml')

    if not os.path.exists(arquivo):
        raise Http404()

    mimetype, encoding = mimetypes.guess_type(arquivo)

    if mimetype is None:
        mimetype = 'application/force-download'

    dados_arquivo = arquivo.split("/")[-1]

    response = HttpResponse(open(arquivo, 'r').read())
    response['Content-Type'] = mimetype
    response['Pragma'] = 'public'
    response['Expires'] = '0'
    response['Cache-Control'] = 'must-revalidate, post-check=0, pre-check=0'
    response['Content-Disposition'] = 'attachment; filename=%s' % dados_arquivo
    response['Content-Transfer-Encoding'] = 'binary'
    response['Content-Length'] = str(os.path.getsize(arquivo))

    return response
