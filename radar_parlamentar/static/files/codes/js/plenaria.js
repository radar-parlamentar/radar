/*##############################################################################
#       Copyright (C) 2016  Diego Rabatone Oliveira, Leonardo Leite,           #
#                           Andres                                             #
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
Plot = (function ($) {

    var idx_votacao = "",
        len_votacoes = 0,
        nome_curto_casa_legislativa = null,
        id_proposicao = null,
        proxima = null,
        anterior = null;

    // Function to load the data and draw the chart
    function initialize(nome_curto_casa_legislativa_, id_proposicao_) {
        //This is just a sample data for tests purposes.
        //d3.json("/analises/json_plenaria/cmsp/100", plot_data);
        nome_curto_casa_legislativa = nome_curto_casa_legislativa_; 
        id_proposicao = id_proposicao_;
        d3.json("/analises/json_plenaria/" + nome_curto_casa_legislativa + "/" + id_proposicao, plot_data);
    }

    // Function that draws the chart
    function plot_data(data) {

//        // Inicialmente remove o spinner de loading
//        $("#loading").remove();

        idx_votacao = get_idx_votacao()
        $( "#votacao" ).text(idx_votacao + 'ª votação');

        var dado = data,
            partidos = data.partidos,
            votacao = data.votacoes[idx_votacao-1],
            parlamentares = votacao.parlamentares;

        len_votacoes = data.votacoes.length;

        var width = 550;
        var height = 300;
        var controle_height = 100;

        var grupo_controle = d3.select("#controle").append("svg")
            .attr("width", width)
            .attr("height", controle_height)
            .append("g");

        var svg = d3.select("#graficoplenaria").append("svg")
          .attr("width", width)
          .attr("height", height)
          .append("g")
          .attr("transform", "translate(280,270)");
 
        anterior = grupo_controle.append("image")
            .attr("xlink:href", "/static/assets/arrow_left.svg")
            .attr("id", "proxima")
            .attr("class", "previous")
            .attr("width", controle_height)
            .attr("height", controle_height);
              
        proxima = grupo_controle.append("image")
            .attr("xlink:href", "/static/assets/arrow_right.svg")
            .attr("id", "anterior")
            .attr("class", "next")
            .attr("x", width - controle_height)
            .attr("width", controle_height)
            .attr("height", controle_height);

        configure_proxima();
        configure_anterior();

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
                .attr("cx", function(parlamentar, i){
                    return escala(i);
                }).attr("r", 5.5) //TODO: Criar uma função para escalar a bolinha proporcionalmente ao número de parlamentares
                .attr("fill", function(parlamentar){
                    return partidos[parlamentar.id_partido].cor;
                }).attr("fill-opacity", 1)
                .attr("stroke", "#000")
                .attr("stroke-width", 0)
                .attr("id", function(parlamentar){
                    return parlamentar.nome;
                }).attr("data-partido", function(parlamentar){
                    return partidos[parlamentar.id_partido].nome;
                }).attr("alt", function(parlamentar){
                    return parlamentar.nome + " - " + partidos[parlamentar.id_partido].nome;
                }).attr("title", function(parlamentar){
                    return parlamentar.nome + " - " + partidos[parlamentar.id_partido].nome;
                }).attr('data-destacado', 0)
                .attr("data-voto", function(parlamentar){
                    return parlamentar.voto;
                }).attr("data-cor-partido", function(parlamentar){
                    return partidos[parlamentar.id_partido].cor;
                }).on('click', function(d){
                    if (d3.select(this).attr("data-destacado") == 1){
                        d3.selectAll('circle')
                          .attr('data-destacado', 0)
                          .attr('fill-opacity', 1)
                          .attr('stroke-width', 0);
                    } else {
                        d3.selectAll('circle')
                          .attr('data-destacado', function(c) { return c.nome==d.nome ? 1 : 0 })
                          .attr('fill-opacity', function(c) { return c.nome==d.nome ? 1 : 0.2 })
                          .attr('stroke-width', function(c) { return c.nome==d.nome ? 1 : 0 });

                        msg = 'Nome: ' + d.nome + '\n';
                        msg = msg + 'Partido: ' + partidos[d.id_partido].nome;
                        msg = msg + ' ('+ partidos[d.id_partido].numero +')\n';
                        msg = msg + 'Voto: ' + d.voto;
                        // TODO: Enviar este conteúdo para uma div apresentável ....
                        console.log(msg);
                    }
                });
    }

    function get_idx_votacao() {
        var idx_votacao = window.location.hash.substr(1);
        if (idx_votacao == "") {
            idx_votacao = 1;
        }
        return idx_votacao
    }

    function configure_proxima() {
        proxima
            .on("mouseover", mouseover_next)
            .on("mouseout", mouseout_next)
            .on("click", proxima_votacao);
    }

    function configure_anterior() {
        anterior
            .on("mouseover", mouseover_previous)
            .on("mouseout", mouseout_previous)
            .on("click", votacao_anterior);
    }

    function mouseover_next() {
        if (proxima_votacao_valida()) {
            proxima.classed("active", true);
            proxima.transition()
                .attr("xlink:href", "/static/assets/arrow_right_focused.svg")
        }
    }

    function mouseout_next() {
        proxima.classed("active", false);
        proxima.transition()
            .attr("xlink:href", "/static/assets/arrow_right.svg")
    }

    function mouseover_previous() {
        if (votacao_anterior_valida()) { 
			anterior.classed("active", true);
            anterior.transition()
                .attr("xlink:href", "/static/assets/arrow_left_focused.svg")
        }
    }

    function mouseout_previous() {
        anterior.classed("active", false);
        anterior.transition()
            .attr("xlink:href", "/static/assets/arrow_left.svg")            
    }


    function proxima_votacao() {
        if (proxima_votacao_valida()) { 
            idx_votacao = idx_votacao + 1
            change_votacao();     
        }
    }

    function votacao_anterior() {
        if (votacao_anterior_valida()) {
            idx_votacao = idx_votacao - 1
            change_votacao();   
        }
    }
    
    function proxima_votacao_valida() {
        return idx_votacao < len_votacoes;
    }
    
    function votacao_anterior_valida() {
        return idx_votacao > 1;
    }
    
    function change_votacao() {
        if(!votacao_anterior_valida()) {
            anterior.classed("invalid", true);
        } else {
            anterior.classed("invalid", false);
        }

        if(!proxima_votacao_valida()) {
            proxima.classed("invalid", true);
        } else {
            proxima.classed("invalid", false);
        }    
    
        atualiza_grafico();
    }

    function atualiza_grafico() {
        window.location.hash = idx_votacao;
        $("#controle").empty();
        $("#graficoplenaria").empty();
        initialize(nome_curto_casa_legislativa, id_proposicao);
    }


    return {
        initialize: initialize
    };
})(jQuery);

function destacarVoto(voto){
    d3.selectAll("circle").each(function(d,i){
        var el = d3.select(this);
        if (el.attr("data-voto")==voto) {
            el.attr("fill", el.attr("data-cor-partido"));
        } else {
            el.attr("fill", "#ccc");
        }
    })
}
