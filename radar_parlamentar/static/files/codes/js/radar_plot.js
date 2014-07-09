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

// Versão para o hackathon cdep 2013

d3.selection.prototype.moveToFront = function() {
  return this.each(function(){
    this.parentNode.appendChild(this);
  });
};

Plot = (function ($) {

    // Function to load the data and draw the chart
    function initialize(nome_curto_casa_legislativa, periodicidade, palavras_chave) {
        if (palavras_chave == "") {
            d3.json("/analises/json_analise/" + nome_curto_casa_legislativa + "/" + periodicidade, plot_data);
        } else {
            d3.json("/analises/json_analise/" + nome_curto_casa_legislativa + "/" + periodicidade + "/" + palavras_chave, plot_data);
        }

        //para testes com arquivo hardcoded
//        d3.json("/static/files/partidos.json", plot_data);
//        d3.json("/static/files/cdep.json", plot_data);
    }

    function space_to_underline(name) {
        return name.replace(/\s+/g,'_');
    }
    
    function cor(d) { return d.cor; }    
    function nome(d) { return space_to_underline(d.nome); } 
    function numero(d) { return d.numero; } 
    
    // Creates a "radialGradient"* for each circle
    // and returns the id of the just created gradient.
    // * the "radialGradient" is a SVG element
    function gradiente(svg,id,color) {
        DEFAULT_COLOR = "#1F77B4";
        if (color === "#000000") color = DEFAULT_COLOR;
        pct_white = 70;
        center_color = shadeColor(color,pct_white); 
        var identificador = "gradient-" + id;
        var gradient = svg.append("svg:defs")
            .append("svg:radialGradient")
            .attr("id", identificador)
            .attr("x1", "0%")
            .attr("y1", "0%")
            .attr("x2", "100%")
            .attr("y2", "100%")
            .attr("spreadMethod", "pad");
        
        gradient.append("svg:stop")
            .attr("offset", "0%")
            .attr("stop-color", center_color)
            .attr("stop-opacity", 1);
        
        gradient.append("svg:stop")
            .attr("offset", "70%")
            .attr("stop-color", color)
            .attr("stop-opacity", 1);
        return "url(#" + identificador + ")";
    }
    
    // Add white to the color. from http://stackoverflow.com/questions/5560248/programmatically-lighten-or-darken-a-hex-color
    function shadeColor(color, percent) {

        var R = parseInt(color.substring(1,3),16);
        var G = parseInt(color.substring(3,5),16);
        var B = parseInt(color.substring(5,7),16);

        R = parseInt(R * (100 + percent) / 100);
        G = parseInt(G * (100 + percent) / 100);
        B = parseInt(B * (100 + percent) / 100);

        R = (R<255)?R:255;  
        G = (G<255)?G:255;  
        B = (B<255)?B:255;  

        var RR = ((R.toString(16).length==1)?"0"+R.toString(16):R.toString(16));
        var GG = ((G.toString(16).length==1)?"0"+G.toString(16):G.toString(16));
        var BB = ((B.toString(16).length==1)?"0"+B.toString(16):B.toString(16));

        return "#"+RR+GG+BB;
    }

    // Chart dimensions.
    var margin = {top: 20, right: 20, bottom: 20, left: 20},
        width_graph = 670,
        height_graph = 670,
        width = width_graph - margin.right - margin.left,
        height = height_graph - margin.top - margin.bottom,
        space_between_graph_and_control = 60,
        height_of_control = 80;
    var TEMPO_ANIMACAO = 500,
        RAIO_PARLAMENTAR = 6;

    // Variables related to the background of concentrical circles
    var radius = 10;
    var dist_between_radiusses = 40;
    var full_radius = Math.min(width,height)/2;
    var bg_radius_array = [radius];
    var bg_radius_index = [0];
    var i = 1;
    radius = radius + dist_between_radiusses;
    while (radius < full_radius) {
//        fundo.append("circle")
//            .attr("class", "background_radius")
//            .attr("r",radius);
        bg_radius_array.push(radius);
        bg_radius_index.push(i++);
        radius = radius + dist_between_radiusses;
    }

    // Scales
    var xScale = d3.scale.linear().range([0, width]), // scale for members
        yScale = d3.scale.linear().range([height, 0]),
        xScalePart = d3.scale.linear().range([0, width]), // scale for parties
        yScalePart = d3.scale.linear().range([height, 0]);

    var periodo_min,
        periodo_max,
        periodo_de,
        periodo_para,
        periodo_atual,
        partidos,
        periodos,
        partidos_explodidos = [];

    // Function that draws the chart
    function plot_data(dados) {

        // Inicialmente remove o spinner de loading
        $("#loading").remove();

        plot_total_votacoes_filtradas(dados["geral"]);

        var r_maximo = dados.max_raio
        var r_partidos = dados.max_raio_partidos
        xScale.domain([-r_maximo, r_maximo])
        yScale.domain([-r_maximo, r_maximo])
//        xScalePart.domain([-r_partidos, r_partidos])
//        yScalePart.domain([-r_partidos, r_partidos])
        xScalePart.domain([-r_maximo, r_maximo])
        yScalePart.domain([-r_maximo, r_maximo])
        
        // Creates the SVG container and sets the origin.
        var svg_base = d3.select("#animacao").append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom + space_between_graph_and_control)
            .style("position", "relative");

        var grupo_controle_periodos = svg_base.append("g")
            .attr("width", width)
            .attr("height", height_of_control)
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        grupo_grafico = svg_base.append("g")
            .attr("id", "grupo_grafico")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .attr("transform", "translate(" + margin.left + "," + (margin.top + space_between_graph_and_control ) + ")");

        var bg_group = grupo_grafico.append("g")
            .attr("transform","translate(" + width/2 + "," + height/2 + ")")
            .attr("id","bg_group");

        legend = d3.selectAll('.legend');

        createBackground(full_radius);
        transitionBackground("linear");

        var label_periodo = grupo_controle_periodos.append("text")
            .attr("class", "year label")
            .attr("text-anchor", "middle")
            .attr("y", 30 )
            .attr("x", width/2);

        var label_nvotacoes = grupo_controle_periodos.append("text")
            .attr("class", "total_label")
            .attr("text-anchor", "middle")
            .attr("y", "48")
            .attr("x", width/2);

        var go_to_previous = grupo_controle_periodos.append("image")
            .attr("xlink:href", "/static/assets/arrow_left.svg")
            .attr("id", "previous_period")
            .attr("class", "previous")
            .attr("y", 0)
            .attr("x", 10)
            .attr("width", 113)
            .attr("height", 113);

        var go_to_next = grupo_controle_periodos.append("image")
            .attr("xlink:href", "/static/assets/arrow_right.svg")
            .attr("id", "next_period")
            .attr("class", "next")
            .attr("y", 0)
            .attr("x", width-113-10)
            .attr("width", 113)
            .attr("height", 113);
        
        // setando variáveis já declaradas
        partidos = dados.partidos;
        periodos = dados.periodos;
        periodo_min = 0;
        periodo_max = periodos.length-1;
        periodo_atual = periodo_min;
        periodo_para = periodo_atual;
        periodo_de = periodo_atual;        

        configure_go_to_next();
        configure_go_to_previous();

        change_period();

        var escala_quadratica = false;

        var alternador_escalas = grupo_controle_periodos.append("text")
            .attr("id", "alterna_escalas")
            .attr("class", "alterna_escala")
            .attr("text-anchor", "middle")
            .attr("y", 130)
            .attr("x", width-40 )
            .text("Zoom In")
            .on("click", alternar_escalas);

        function alternar_escalas() {
            if (escala_quadratica==false) {
                xScale = d3.scale.sqrt();
                yScale = d3.scale.sqrt();
                xScalePart = d3.scale.sqrt();
                yScalePart = d3.scale.sqrt();
                escala_quadratica = true;
                alternador_escalas.text("Zoom Out");
                transitionBackground("quadratic");
            }
            else {
                xScale = d3.scale.linear();
                yScale = d3.scale.linear();
                xScalePart = d3.scale.linear();
                yScalePart = d3.scale.linear();
                escala_quadratica = false;
                alternador_escalas.text("Zoom In");
                transitionBackground("linear");
            }
            xScale.range([0, width]).domain([-r_maximo, r_maximo]); // scale for members
            yScale.range([height, 0]).domain([-r_maximo, r_maximo]);
            xScalePart.range([0, width]).domain([-r_maximo, r_maximo]); // scale for parties
            yScalePart.range([height, 0]).domain([-r_maximo, r_maximo]);
            atualiza_grafico(true);
        }

        var explodidor_todos = grupo_grafico.append("text")
            .attr("id", "explodidor_todos")
            .attr("class", "alterna_escala")
            .attr("text-anchor", "middle")
            .attr("y", height-50)
            .attr("x", width-50 )
            .text("Expandir Todos")
            .on("click", explode_todos);

        var implodidor_todos = grupo_grafico.append("text")
            .attr("id", "implodidor_todos")
            .attr("class", "alterna_escala")
            .attr("text-anchor", "middle")
            .attr("y", height-30)
            .attr("x", width-50 )
            .text("Recolher Todos")
            .on("click", implode_todos);

        // ############## Funções de controle de mudanças de estado ###########
        
        // Função que controla mudança de estado para o estado seguinte
        function configure_go_to_next() {
            go_to_next
                .on("mouseover", mouseover_next)
                .on("mouseout", mouseout_next)
                .on("click", change_to_next_period);
        }

        // Função que controla a mudança de estado para o estado anterior
        function configure_go_to_previous() {
            go_to_previous
                .on("mouseover", mouseover_previous)
                .on("mouseout", mouseout_previous)
                .on("click", change_to_previous_period);
        }
        
        function change_to_next_period() {
            if (periodo_atual < periodo_max) { 
                periodo_de = periodo_atual;
                periodo_para = periodo_atual + 1;
                periodo_atual = periodo_para;
                change_period();
            }
        }

        function change_to_previous_period() {
            if (periodo_atual > periodo_min) {
                periodo_de = periodo_atual;
                periodo_para = periodo_atual - 1;
                periodo_atual = periodo_para;
                change_period();
            }
        }
        
        function change_period() {
            atualiza_grafico(false);
        }

        // atualiza partidos e deputados no gráfico de acordo com o período atual
        // explodindo: true quando estamos atualizando o gráfico por causa de uma explosão de partido
        // (explosão de partido é quando se clica no partido para ver seus parlamentares)
        function atualiza_grafico(explodindo) {
            label_nvotacoes.text("Não há votações relacionadas com as palavras chave informadas");

            // Legend
            var partidos_legenda = get_partidos_no_periodo(periodo_atual);

            var legend_items = legend.selectAll('.legend_item')
                .data(partidos_legenda, function(d) {return d.nome});
            legend_items.transition()
                .text(function(d) {return d.numero + " | " + d.nome + " (" + d.t[periodo_atual] + ")"})
                .duration(TEMPO_ANIMACAO);
            var new_legend_items = legend_items.enter().append("li")
                .attr("class","legend_item")
                .attr("id", function(d) { return "legend-"+nome(d); })
                .text(function(d) {return d.numero + " | " + d.nome + " (" + d.t[periodo_atual] + ")"})
                .on("mouseover", function(d) { mouseover_legend(d); })
                .on("mouseout", function(d) { mouseout_legend(d); })
                .on("click", function(d) { click_legend(d); });
            legend_items.exit().remove();

            // Circles that represent the parties
            partidos_no_periodo = get_partidos_nao_explodidos_no_periodo(periodo_atual);
            var parties = grupo_grafico.selectAll('.party').data(partidos_no_periodo, function(d) { return d.nome });
            var circles = grupo_grafico.selectAll('.party_circle').data(partidos_no_periodo, function(d) { return d.nome });

            party_tip = d3.tip()
                .attr('class', 'd3-tip')
                .offset([-10,0])
                .html(function(d) { 
                    r = "<strong><span style='color:" + d.cor + ";text-shadow: -1px 0 #333, 0 1px #333, 1px 0 #333, 0 -1px #333'>" + d.numero + " - </span>" + d.nome + "</strong></br>";
                    r += "<strong>Parlamentares:</strong> <span style='color:yellow'>" + d.t[periodo_atual] + "</span></br>";
                    r += "<span style='color:yellow'><strong>Clique para expandir!</strong></span>";
                    return r;
                });


            parties.transition()
                .attr("transform", function(d) { return "translate(" + xScalePart(d.x[periodo_para]) +"," +  yScalePart(d.y[periodo_para]) + ")" })
                .duration(TEMPO_ANIMACAO);
            
            parties.selectAll(".party_circle").transition()
                .attr("r", function(d) { return d.r[periodo_para]})
                .duration(TEMPO_ANIMACAO);

            svg_base.call(party_tip);

            var new_parties = parties.enter().append("g")
                .attr("class","party")
                .attr("id",function(d){return "group-"+nome(d);})
                .attr("transform", function(d) { return "translate(" + xScalePart(d.x[periodo_atual]) +"," +  yScalePart(d.y[periodo_atual]) + ")";})
                .attr("opacity",0.00001);

            // title is used for the browser tooltip
//            new_parties.append("title")
//                .text(function(d) { return nome(d); });
    
            var new_circles = new_parties.append("circle")
                .attr("class","party_circle")
                .attr("id", function(d) { return "circle-" + nome(d); })
                .attr("r", 0)
                .attr("fill", function(d) {return gradiente(grupo_grafico, nome(d), cor(d)); });

            new_parties.append("text")
                .attr("text-anchor","middle")
                .attr("dy",3)
                .text(function(d) { return d.nome; });

            // o circulo abaixo é totalmente transparente mas serve para os eventos de mouse,
            // pois ele fica em cima do circulo do partido e em cima do texto.
            new_parties.append("circle")
                .attr("r", function(d) {return d.r[periodo_atual]; })
                .attr("opacity",0.0)
                .on("mouseover", function(d) { return mouseover_party(d); })
                .on("mouseout", function(d) { return mouseout_party(d); })
                .on("click", function(d) { return explode_partido(d); });

            new_parties.transition()
                .attr("opacity",1)
                .duration(TEMPO_ANIMACAO);

            new_circles.transition().duration(TEMPO_ANIMACAO)
                .attr("r", function(d) { return d.r[periodo_atual]; });
            
            // tirar os parlamentares eventualmente explodidos que pertencam a partidos que estejam saindo de cena:
            partidos_ou_parlamentares_no_periodo = get_partidos_no_periodo(periodo_atual);
            var parties2 = grupo_grafico.selectAll('.party').data(partidos_ou_parlamentares_no_periodo, function(d) { return d.nome });
            var parties_vao_sair2 = parties2.exit();
            var partidos_ausentes = get_partidos_ausentes_no_periodo(periodo_atual);
            partidos_ausentes.forEach(function(vai_sair){
                parlam_vai_sair = grupo_grafico.selectAll(".partido_" + nome(vai_sair));
                parlam_vai_sair.remove();
            })

            circles.exit().transition().duration(TEMPO_ANIMACAO).attr("r",0).remove();
            var parties_vao_sair = parties.exit().transition().duration(TEMPO_ANIMACAO);
            parties_vao_sair.remove();

            parlamentar_tip = d3.tip()
                .attr('class', 'd3-tip')
                .offset([-10,0])
                .html(function(d) { 
                    var r = "<strong> " + d.nome + " <span style='color:yellow'>" + d.partido + "</span>-<span style='color:yellow'>" + d.localidade + "</span></br>";
                    r += "<span style='color:yellow'><strong>Clique para recolher!</strong></span>";
                    return r;
                });

            svg_base.call(parlamentar_tip);

            // Parlamentares (represented by dots), treating one party at a time in this loop:
            partidos_legenda.forEach(function(partido) {
                if (jQuery.inArray(partido,partidos_explodidos) == -1)
                    var parlamentares_no_periodo = []; // não é para ter dados de parlamentares se o partido não estiver explodido.
                else
                    var parlamentares_no_periodo = get_parlamentares_no_periodo(partido, periodo_atual);

                // DATA-JOIN dos parlamentares deste partido:
                var parlamentares = grupo_grafico.selectAll('.parlamentar_circle.partido_' + nome(partido))
                    .data(parlamentares_no_periodo, function(d) { return d.id });

                parlamentares.transition()
                             .duration(TEMPO_ANIMACAO)
                             .attr("cx", function(d) { return xScale(d.x[periodo_para]); })
                             .attr("cy", function(d) { return yScale(d.y[periodo_para]); });

                var new_parlamentares = parlamentares.enter().append("circle")
                    .attr("class",["parlamentar_circle partido_" + nome(partido)] )
                    .attr("id", function(d) { return "point-" + nome(d); })
                    .attr("r", RAIO_PARLAMENTAR)
                    .attr("fill", cor(partido))
                    .on("mouseover", function(d) {d["partido"] = partido.nome; return mouseover_parlamentar(d); })
                    .on("mouseout", function(d) {return mouseout_parlamentar(d); })
                    .on("click", function(d) { return implode_partido(partido); });

                if (explodindo) {
                    new_parlamentares.attr("cx", xScale(partido.x[periodo_atual]))
                                     .attr("cy", yScale(partido.y[periodo_atual]))
                                     .transition().duration(TEMPO_ANIMACAO)
                                                  .attr("cx", function(d) { return xScale(d.x[periodo_atual]); })
                                                  .attr("cy", function(d) { return yScale(d.y[periodo_atual]); });

                    parlamentares.exit()
                        .attr("cx", function(d) { return xScale(d.x[periodo_atual]); })
                        .attr("cy", function(d) { return yScale(d.y[periodo_atual]); })
                        .transition().duration(TEMPO_ANIMACAO)
                                     .attr("cx", xScale(partido.x[periodo_atual]))
                                     .attr("cy", yScale(partido.y[periodo_atual]))
                        .remove();
                } else {
                    new_parlamentares.attr("cx", function (d) { return xScale(d.x[periodo_para]); })
                                     .attr("cy", function (d) { return yScale(d.y[periodo_para]); })
                                     .attr("r",0);
                    new_parlamentares.transition()
                                     .duration(TEMPO_ANIMACAO)
                                     .attr("r", RAIO_PARLAMENTAR);

                    parlamentares.exit().transition().duration(TEMPO_ANIMACAO).attr("r",0).remove();
                }
            });            
            
            label_periodo.text(periodos[periodo_atual].nome);
            quantidade_votacoes = periodos[periodo_atual].nvotacoes;
            label_nvotacoes.text(quantidade_votacoes + " votações"); 
            
            sortAll();
            
            if (periodo_para == periodo_max) mouseout_next();
            if (periodo_para == periodo_min) mouseout_previous();
        }

        function mouseover_legend(party) {
            d3.selectAll("#circle-"+nome(party)).classed("hover",true);
            d3.selectAll("#group-"+nome(party)).moveToFront();
            d3.selectAll("#legend-"+nome(party)).classed("active",true);
            d3.selectAll('.partido_' + nome(party)).attr("class",["parlamentar_circle_hover partido_" + nome(party)] );
        }
        
        function mouseout_legend(party) {
            d3.selectAll("#circle-"+nome(party)).classed("hover",false);
            d3.selectAll("#legend-"+nome(party)).classed("active",false);
            d3.selectAll('.partido_' + nome(party)).attr("class",["parlamentar_circle partido_" + nome(party)] );
            sortAll();
        }

        function click_legend(party) {
            return;
        }

        function mouseover_party(party) {
            var circulo = d3.selectAll("#circle-"+nome(party)).classed("hover",true);
//            d3.selectAll("#group-"+nome(party)).moveToFront(); // 
            d3.selectAll("#legend-"+nome(party)).classed("active",true);
            party_tip.show(party);
        }
        
        function mouseout_party(party) {
            d3.selectAll("#circle-"+nome(party)).classed("hover",false);
            d3.selectAll("#legend-"+nome(party)).classed("active",false);
            party_tip.hide();
//            sortAll();
        }

        function mouseover_parlamentar(parlamentar) {
//            var circulo = d3.selectAll("#circle-"+nome(party)).classed("hover",true);
//            d3.selectAll("#legend-"+nome(party)).classed("active",true);
            parlamentar_tip.show(parlamentar);
        }
        
        function mouseout_parlamentar(parlamentar) {
            parlamentar_tip.hide();
        }


        function mouseover_next() {
            if (periodo_atual < periodo_max) {
                go_to_next.classed("active", true);
                go_to_next.transition()
                    .attr("xlink:href", "/static/assets/arrow_right_focused.svg")
            }
        }

        function mouseout_next() {
            go_to_next.classed("active", false);
            go_to_next.transition()
                .attr("xlink:href", "/static/assets/arrow_right.svg")
        }

        function mouseover_previous() {
            if (periodo_atual > periodo_min) { 
                go_to_previous.classed("active", true);
                go_to_previous.transition()
                    .attr("xlink:href", "/static/assets/arrow_left_focused.svg")
            }
        }

        function mouseout_previous() {
            go_to_previous.classed("active", false);
            go_to_previous.transition()
                .attr("xlink:href", "/static/assets/arrow_left.svg")            
        }
        
        function sortAll() {
            var circunferencias = grupo_grafico.selectAll(".party, .parlamentar_circle");
            circunferencias.sort(order);
            var legend_entries = legend.selectAll(".legend_item");
            legend_entries.sort(order);
        }

        function explode_partido(partido) { //partido é o json do partido
            party_tip.hide();
            partidos_explodidos.push(partido);
            atualiza_grafico(true);
        }
        
        function implode_partido(partido) { //partido é o json do partido
            parlamentar_tip.hide();
            remove_from_array(partidos_explodidos,partido);
            atualiza_grafico(true);
        }

        function explode_todos() {
            party_tip.hide();
            partidos_explodidos = get_partidos_no_periodo(periodo_atual);
            atualiza_grafico(true);
        }

        function implode_todos() {
            parlamentar_tip.hide();
            partidos_explodidos = [];
            atualiza_grafico(true);
        }

        // remove o elemento de valor el da array lista, e retorna a lista modificada
        function remove_from_array(lista,el) {
            for(var i = lista.length - 1; i >= 0; i--) {
                if(lista[i] === el) {
                    lista.splice(i, 1);
                }
            }
            return lista;
        }

        // Defines a sort order so that the smallest parties are drawn on top.
        function order(a, b) {
            if (a == null || b == null) console.log(parties, a, b);
            if (is_parlamentar(a))
                return 1
            if (is_parlamentar(b))
                return -1
            return b.t[periodo_atual] - a.t[periodo_atual];
        }
        
        function is_parlamentar(d) {
            // bem hacker ^^
            return (typeof d.cor === "undefined")
        }

//        function moveToFront(party) {
//            return this.each(function(){
//                this.parentNode.appendChild(this);
//            });
//        }


        // Retorna partidos excluindo partidos ausentes no período
        function get_partidos_no_periodo(period) {
            return partidos.filter(function(d){ return d.t[period] > 0;});
        }

        function get_partidos_ausentes_no_periodo(period) {
            return partidos.filter(function(d){ return d.t[period] == 0;});
        }

        // Retorna partidos excluindo partidos ausentes no período e partidos explodidos
        function get_partidos_nao_explodidos_no_periodo(period) {
            return partidos.filter(function(d){ return d.t[period] > 0 && jQuery.inArray(d,partidos_explodidos) == -1;});
        }
        
        // Retorna o json de parlamentares do partido, do qual foram excluídos parlamentares ausentes no dado period.
        function get_parlamentares_no_periodo(partido, period) {
            return partido.parlamentares.filter(function (d) {return d.x[periodo_atual] !== null; })
        }
    }

    function plot_total_votacoes_filtradas(dados_gerais) {
        if (dados_gerais["palavras_chaves"].length > 0) {
          total_votacoes_filtradas = dados_gerais["total_votacoes"]

          if (total_votacoes_filtradas == 0) {
            $("#veja_as_votacoes").attr("hidden", true)
          }

          $( "#total_votacoes_filtradas_div" ).show()
          $( "#total_votacoes_filtradas" ).text(total_votacoes_filtradas);
        }
    }

    function createBackground(full_radius) {
        background = grupo_grafico.append("g")
            .attr("transform","translate(" + width/2 + "," + height/2 + ")")
            .attr("id","background");
        background.append("circle")
            .attr("class","outer_background_radius")
            .attr("r",full_radius);
    }

    function transitionBackground(type_of_scale) {
        // type_of_scale should be a string, either "linear" or "quadratic"                
        var local_radius_array = bg_radius_array; // fallback to linear scale.
        if (type_of_scale == "linear") {
            var local_radius_array = bg_radius_array;
        }
        else if (type_of_scale == "quadratic") {
            var local_radius_array = bg_radius_array.map(function(d) {return Math.sqrt(d/full_radius)*full_radius });
        }
        // DATA-JOIN
        var bg_circles = background.selectAll('.background_radius').data(bg_radius_index);

        // TRANSITION
        bg_circles.transition()
            .duration(TEMPO_ANIMACAO)
            .attr("r", function(d) { return local_radius_array[d]});

        // ENTER
        var new_circles = bg_circles.enter().append("circle")
            .attr("class","background_radius")
            .attr("r", function(d) { return local_radius_array[d]});
    }

    return {
        initialize:initialize
    };
})(jQuery);
