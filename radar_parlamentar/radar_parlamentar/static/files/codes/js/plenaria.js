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
        identificador_proposicao = null,
        proxima = null,
        anterior = null,
        dado = null;


    // Function to load the data and draw the chart
    function initialize(nome_curto_casa_legislativa_, identificador_proposicao_) {
        nome_curto_casa_legislativa = nome_curto_casa_legislativa_;
        identificador_proposicao = identificador_proposicao_;
        d3.json("/plenaria/json/" + nome_curto_casa_legislativa + "/" + identificador_proposicao + "/", first_plot);
    }

    function first_plot(data) {

        // Inicialmente remove o spinner de loading
        $("#loading").remove();
        dado = data;
        len_votacoes = data.votacoes.length;

        $(dado.votacoes).each(function(idx) {
            jQuery("<input/>", {
                type: "button",
                name: 'votacao-'+ idx,
                class: "botao escolhe-votacao",
                value: (idx+1) + "ª votação",
                onClick: "window.location.hash = " + (idx+1) + "; window.plot_data(); atualiza_botao_votacao(this);"
            }).appendTo('#votacoes');
        });
        idx_votacao = get_idx_votacao();
        var botao = idx_votacao - 1
        $('[name="votacao-'+botao+'"]').addClass('ativado');

        plot_data();
    }

    // Function that draws the chart
    function plot_data() {

        $("#controle").empty();
        $("#graficoplenaria").empty();

        // Inicialmente remove o spinner de loading
        $("#loading").remove();
        $(".d3-tip").remove();

        idx_votacao = get_idx_votacao();

        var partidos = dado.partidos,
            votacao = dado.votacoes[idx_votacao-1],
            parlamentares = votacao.parlamentares;

        $('#prop_ementa').html(dado.ementa)
        $('#prop_descr').html(dado.descricao)
        $('#votacao_data').html('Data: ' + votacao.data)
        $('#votacao_descr').html('Descrição: ' + votacao.descricao)
        $('#votacao_resultado').html('Resultado: ' + votacao.resultado)

        parlamentar_tooltip = d3.tip()
            .attr('class', 'd3-tip')
            .html(function(parlamentar) {
                var atributo = "<strong>Nome:</strong> <span style='color:yellow'>" + parlamentar.nome + "</span></br>";
                atributo += "<strong>Partido:</strong> <span style='color:yellow'>" + partidos[parlamentar.id_partido].nome + "</span></br>";
                atributo += "<strong>Voto:</strong> <span style='color:yellow'>" + parlamentar.voto + "</span></br>";
                return atributo;
            })
            .style('text-align','left');

        len_votacoes = dado.votacoes.length;

        var width = 550;
        var height = 300;

        var svg = d3.select("#graficoplenaria").append("svg")
          .attr("width", width)
          .attr("height", height)
          .append("g")
          .attr("transform", "translate(280,270)")
          .call(parlamentar_tooltip);

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
                }).attr("r", 8) //TODO: Criar uma função para escalar a bolinha proporcionalmente ao número de parlamentares
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
                    var div = $("#detalheParlamentar");
                    if (d3.select(this).attr("data-destacado") == 1){
                        d3.selectAll('circle')
                          .attr('data-destacado', 0)
                          .attr("fill", function(c){ return partidos[c.id_partido].cor; })
                          .attr('fill-opacity', 1)
                          .attr('stroke-width', 0);
                        div.empty();
                    } else {
                        d3.selectAll('circle')
                          .attr('data-destacado', function(c) { return c.nome==d.nome ? 1 : 0 })
                          .attr("fill", function(c){ return partidos[c.id_partido].cor; })
                          .attr('fill-opacity', function(c) { return c.nome==d.nome ? 1 : 0.2 })
                          .attr('stroke-width', function(c) { return c.nome==d.nome ? 1 : 0 });

                        div.empty();
                        div.append('<p><b>Nome: </b>' + d.nome + '</p>')
                        div.append('<p><b>Partido: </b>' + partidos[d.id_partido].nome +
                                   ' ('+ partidos[d.id_partido].numero +')</p>');
                        div.append('<p><b>Voto: </b>' + d.voto + '</p>');
                    }
                }).on('mouseover', function(parlamentar) {
                    return mouseover_parlamentar(parlamentar);
                })
                .on('mouseout', function(parlamentar) {
                    return mouseout_parlamentar(parlamentar);
                });

        document.getElementById('votacoes').scrollIntoView();

    }

    window.plot_data = plot_data

    function get_idx_votacao() {
        var idx_votacao = window.location.hash.substr(1);
        if (idx_votacao == "") {
            idx_votacao = 1;
        }
        return parseInt(idx_votacao);
    }

    return {
        initialize: initialize
    };
    function nome(parlamentar){
        if(parlamentar.nome)
            return parlamentar.nome.replace(".","");
        else
            return "Não possui nome";
    }

    function mouseover_parlamentar(parlamentar) {
        d3.selectAll("#parlamentar-"+nome(parlamentar)).classed("hover",true);
        parlamentar_tooltip.show(parlamentar);

        /* After show, force the tooltip to stay together with circle
        using the position of mouse in the page, obtained from d3.event*/
        d3.select('.d3-tip')
            .style('left',d3.event.pageX-90+'px')
            .style('top',d3.event.pageY-80+'px')
    }

    function mouseout_parlamentar(parlamentar) {
        d3.selectAll("#parlamentar-"+nome(parlamentar)).classed("hover",false);
        parlamentar_tooltip.hide(parlamentar);
    }


})(jQuery);

function atualiza_botao_votacao(el){
    $(".escolhe-votacao").removeClass("ativado");
    $(el).addClass("ativado");
    $(".filtro-voto").removeClass("ativado");
    $("#voto_todos").addClass("ativado");
}


$('.botao').click(function() {
    var voto = $(this).attr("data");
    $("#detalheParlamentar").empty();
    $(".filtro-voto").removeClass("ativado");
    $(this).addClass("ativado");

    situacao_atual = $(".filtro-voto.ativado").val();
    d3.selectAll("circle").each(function(d,i){
        var el = d3.select(this)
                   .attr("data-destacado", 0)
                   .attr("fill-opacity", 1)
                   .attr("stroke-width", 0);
        if (el.attr("data-voto")==voto || voto=="TODOS" || situacao_atual=="TODOS") {
            el.attr("fill", el.attr("data-cor-partido"));
        } else {
            el.attr("fill", "#ccc");
        }
    })
});
