/*##############################################################################
#       Copyright (C) 2013  Diego Rabatone Oliveira, Leonardo Leite,           #
#                           Saulo Trento                                       #
#                                                                              #
#    This program is free software: you can redistribute it and/or modify      #
# it under the terms of the GNU Affero General Public License as published by  #
#      the Free Software Foundation, either version 3 of the License, or       #
#                     (at your option) any later version.                      #
#                                                                              #
#       This program is distributed in the hope that it will be useful,        #
#       but WITHOUT ANY WARRANTY; without even the implied warranty of         #
#        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
#             GNU Affero General Public License for more details.              #
#                                                                              #
#  You should have received a copy of the GNU Affero General Public License    #
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.     #
##############################################################################*/

// Versão para o hackathon 2016

var Plot = (function ($) {

    function set_column_count(el, n) {
        ['-webkit-', '-moz-', ''].forEach(function (t){el.css(t+'column-count', n)})
    }

    function get_cor_parl(dados, parlamentar) {
        return dados.partidos[parlamentar.id_partido].cor
    }

    function get_cor_voto(parlamentar, cor_sim) {
        return parlamentar.voto == 'SIM' ? cor_sim : '#FFF0'
    }

    // Function to load the data and draw the chart
    function initialize(nome_curto_casa_legislativa, cod_proposicao) {
        d3.json("/analises/json_plenaria/" + nome_curto_casa_legislativa + "/" + cod_proposicao, plot_data);
    }

    // Function that draws the chart
    function plot_data(dados) {
        // Inicialmente remove o spinner de loading
        $("#loading").remove();
        console.log(dados)
        var parlamentares = dados.votacoes[0].parlamentares
        parlamentares.forEach(function (parlamentar){
            var cor = get_cor_parl(dados, parlamentar)
            var cor_voto = get_cor_voto(parlamentar, cor)
            var partido = dados.partidos[parlamentar.id_partido].nome
            $('#teatro').append('<div class="parlamentar tooltip" style="background-color:' + cor_voto + ';border: 5px solid '+ cor +';">' + parlamentar.nome[0] + '<span class="tooltiptext">' + parlamentar.nome + ' (' + partido + ')</span></div>')
        })

        var parl_count = parlamentares.length
        var num_col = Math.ceil((parl_count*1.68)**0.5)
        set_column_count($('#teatro'), num_col )


    }

    return {
        initialize:initialize
    };
})(jQuery);
