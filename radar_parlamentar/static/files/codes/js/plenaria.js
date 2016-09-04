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

// d3.selection.prototype.moveToFront = function() {
//   return this.each(function(){
//     this.parentNode.appendChild(this);
//   });
// };

//Plot = (function ($) {
//
//    // Function to load the data and draw the chart
//    function initialize(nome_curto_casa_legislativa, cod_proposicao) {
//        d3.json("/analises/json_teatro/" + nome_curto_casa_legislativa + "/" + cod_proposicao, plot_data);
//    }
//
//    // Function that draws the chart
//    function plot_data(dados) {
//        // Inicialmente remove o spinner de loading
//        $("#loading").remove();
//        alert(dados.nome)
//    }
//
//    return {
//        initialize:initialize
//    };
//})(jQuery);
var dado = undefined,
    partidos = undefined,
    votacao = undefined,
    parlamentares = undefined;

function plot_data(data) {

    dado = data;
    partidos = data.partidos;
    votacao = data.votacoes[0];
    parlamentares = votacao.parlamentares;

    var svg = d3.select("#graficoplenaria").append("svg")
      .attr("width", 550)
      .attr("height", 400)
      .append("g")
      .attr("transform", "translate(280,270)");

    var parlamentares_por_raio = 2,
        raios = [],
        total_de_raios = Math.ceil(parlamentares.length/parlamentares_por_raio);

    for(i=0; i<total_de_raios; i++) {
        raios.push({'angulo': -i*180/( total_de_raios - 1), 'nome': i,
        'lista_de_parlamentares': parlamentares.slice(i*parlamentares_por_raio, i*parlamentares_por_raio+parlamentares_por_raio) });
    }

    var escala = d3.scale.linear().domain([0, parlamentares_por_raio]).range([180, 270]),
          cor = d3.scale.linear().domain([0, parlamentares_por_raio]).range(["brown", "steelblue"]);

    /* Constrói cada uma das linhas radiais */
    var g = svg.selectAll("g")
      .data(raios)
      .enter().append("g")
      .attr("transform", function(raio) {
        return "rotate(" + raio.angulo + ")";
      }).attr("id", function(raio, i){ return i; })
        .selectAll("circle")
            .data(function(raio){return raio.lista_de_parlamentares})
            .enter().append("circle")
            .attr("cx", function(parlamentar, i){ return escala(i);})
            .attr("r", 8.5) //TODO: Criar uma função para escalar a bolinha proporcionalmente ao número de parlamentares
            .attr("fill", function(parlamentar){ return partidos[parlamentar.id_partido].cor; })
            .attr("stroke", "black")
            .attr("id", function(parlamentar){return parlamentar.nome;})
            .attr("data-partido", function(parlamentar){ return partidos[parlamentar.id_partido].nome; })
            .attr("alt", function(parlamentar){ return parlamentar.nome + " - " + partidos[parlamentar.id_partido].nome; })
            .attr("title", function(parlamentar){ return parlamentar.nome + " - " + partidos[parlamentar.id_partido].nome; });

}

// This is just a sample data for tests purposes.
d3.json("/analises/json_plenaria/cmsp/100", plot_data);
