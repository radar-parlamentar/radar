/*##############################################################################
#       Copyright (C) 2013  Diego Rabatone Oliveira, Leonardo Leite            #
#                      <diraol(at)diraol(dot)eng(dot)br>                       #
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

Plot = (function ($) {
  
  function initialize(dataPath){
    _load(dataPath);
  }

  // Function to load the data and draw the chart
  function _load(nome_curto_casa_legislativa) {
    d3.json("/analises/analise/" + nome_curto_casa_legislativa + "/json_pca", _plot_data);
    //para testes com arquivo hardcoded
    //d3.json("/static/files/partidos.json", _plot_data);
  }
  
  function x(d) { return d.x; } // income (per capta) from original json
  function y(d) { return d.y; } // life expectancy from original json
  function tamanho(d) { return d.tamanho; } // population from original json
  function cor(d) { return d.cor; } // based on region from original json
  function nome(d) { return d.nome; } // name from original json
  function numero(d) { return d.numero; } // new parameter to json

  //Create Gradient Fill for each circle
  function gradiente(svg,id,color){
        if (color == "#000000") color = "#1F77B4";
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
            .attr("stop-color", color)
            .attr("stop-opacity", 0.5);

        gradient.append("svg:stop")
            .attr("offset", "70%")
            .attr("stop-color", color)
            .attr("stop-opacity", 1);
        return "url(#" + identificador + ")";
  }

  // Chart dimensions.
  var margin = {top: 20, right: 20, bottom: 20, left: 20},
      width = 670 - margin.right - margin.left;
      height = 670 - margin.top - margin.bottom;
  
  // Various scales. These domains make assumptions of data, naturally.
  var xScale = d3.scale.linear().domain([0, 100]).range([0, width]),
      yScale = d3.scale.linear().domain([0, 100]).range([height, 0]),
      radiusScale = d3.scale.sqrt().domain([0, 9]).range([0, 40]),
      colorScale = d3.scale.category10();
  
  // The x & y axes.
  var xAxis = d3.svg.axis().orient("bottom").scale(xScale).ticks(12, d3.format(",d")),
      yAxis = d3.svg.axis().scale(yScale).orient("left");
  
  //Returns the max and min period
  //  On the JSON the period unique identifier is string representing a unique number for each period.
//  function limit_period(periodArray, choice) {
//    var local_array = [];
//    for (var period in periodArray) {
//      local_array.push(parseInt(period));
//    }



  // Function that draw the chart
  function _plot_data(dados) {
    // Various accessors that specify the four dimensions of data to visualize.
    //
    // First remove the spinner
    $("#loading").remove();
    
      
    // Create the SVG container and set the origin.
    var svg = d3.select("#animacao").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .style("position", "relative")
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
    
    //Adicionando o fundo do radar
    var fundo = svg.append("g")
          .attr("class","radar")
          .attr("transform","translate(" + width/2 + "," + height/2 + ")");
    
    raio_fundo = (width > height) ? height/2 : width/2;
    
    fundo.append("circle")
          .attr("class", "radar_background")
          .attr("r", raio_fundo);
    
    raio = 10;
    while (raio < raio_fundo) {
        fundo.append("circle")
            .attr("class", "raio_radar")
            .attr("r",raio);
        raio = raio + 40;
    }

    var partidos = dados.partidos,
        periodos = dados.periodos,
        list_partds = []
        list_periodos = [];
    
    //Carregando os períodos extremos dos dados
    var chaves_periodos = d3.keys(periodos),
        lista_periodos = [];
        for (item in chaves_periodos) { lista_periodos.push( parseInt( chaves_periodos[item] ) ); };
    
    var periodo_min = d3.min(lista_periodos),
        periodo_max = d3.max(lista_periodos);

    first_label = periodos[periodo_min].nome;
    first_total = periodos[periodo_min].quantidade_votacoes;

    // Add the year label; the value is set on transition.
    var label = svg.append("text")
        .attr("class", "year label")
        .attr("text-anchor", "end")
        .attr("y", '34')
        .attr("x", width + margin.right)
        .text(first_label);
    
    var total_label = svg.append("text")
        .attr("class", "total_label")
        .attr("text-anchor", "end")
        .attr("y", "50")
        .attr("x", width + margin.right)
        .text("Votações analisadas no período: " + first_total + " votações")
    
    // A bisector since many nation's data is sparsely-defined.
    var bisect = d3.bisector(function(d) { return d[0]; });

    // Add a partie. Initialize the date at 1800, and set the colors.
    var main = svg.append("g")
                        .attr("id","parties")
    
    var dados = interpolateData(1)
            .filter(function(d){ return d.tamanho;});

    var parties = main.selectAll(".partie")
            .data(dados)
          .enter().append("g")
            .attr("class","partie")
            .attr("id", function(d){return "group-"+nome(d);})
            .attr("transform", function(d) { return "translate(" + xScale(x(d)) +"," +  yScale(y(d)) + ")";});
    
    parties.append("circle")
            .attr("class", "partie_circle")
            .attr("id", function(d) { return "circle-" + nome(d); })
            .style("fill", function(d) { return gradiente(svg, nome(d), cor(d)); }) // colorScale(cor(d)); })
            .attr("r", function(d) { return radiusScale(tamanho(d)); });
            //.call(position)
    
    // Add a title.
    parties.append("title")
        .text(function(d) { return nome(d); });
   
    parties.append("text")
            .text(function(d){ return numero(d);})
                //.attr("x", function(d) {return x(d);})
                //.attr("y", function(d) {return y(d);})
                .attr("dx", "-8")
                .attr("dy", "3")
                /*.attr("textLength", function(d){ return radiusScale(tamanho(d));})
                .attr("lengthAdjust", "spacingAndGlyphs")*/
            //.call(position_text)

    parties.sort(order)

    // Add an overlay for the year label.
    var l_box = label.node().getBBox();

    var overlay = svg.append("rect")
          .attr("class", "overlay")
          .attr("x", l_box.x)
          .attr("y", l_box.y)
          .attr("width", l_box.width)
          .attr("height", l_box.height)
          .on("mouseover", enableInteraction);
    
    // Start a transition that interpolates the data based on year.
    svg.transition()
        .duration(10000)
        .ease("linear")
        .tween("year", tweenYear)
        .each("end", enableInteraction);
 
    /* TODO */
    function redraw_parties(period) {

        dados = interpolateData(period);

        partie_group = svg.selectAll(".partie_group")
                .data(dados.filter(function(d){ return d.tamanho;}),name);
        
        /* Adicionando novos elementos e atualizando antigos */
        partie_group.enter().append("g")
            .attr("class", "partie_group")
            .attr("id", function(d){return "group-"+nome(d);})
            .sort(order);

        /* Removendo elementos não mais existentes */
        partie_group.exit().remove();
        
        partie_group.append("circle")
            .attr("class", "partie")
            .attr("id", function(d) { return "circle-" + nome(d); })
            .style("fill", function(d) { return gradiente(svg, nome(d), cor(d)); }) // colorScale(cor(d)); })
            .call(position)
        
        partie_group.append("text")
            .text(function(d){return nome(d);})
            //.attr("x", function(d) {return x(d);})
            //.attr("y", function(d) {return y(d);})
            .attr("dx", "-10")
            /*.attr("textLength", function(d){ return radiusScale(tamanho(d));})
            .attr("lengthAdjust", "spacingAndGlyphs")*/
            //.call(position_text)

        // Add a title.
        partie_group.append("title")
            .text(function(d) { return numero(d); });
   
        /* Removendo elementos não mais existentes */
        partie_group.exit().remove();

        label.text(periodos[Math.round(period)].nome);
        quantidade_votacoes = periodos[Math.round(period)].quantidade_votacoes
        total_label.text(quantidade_votacoes + " votações");
        
    }

    // Positions the texto over the parties based on data.
    function position_text(partie) {
      partie.attr("x", function(d) { return xScale(x(d)); })
          .attr("y", function(d) { return yScale(y(d)); })
    }

    // Positions the parties based on data.
    function position(partie) {
      partie.attr("cx", function(d) { return xScale(x(d)); })
          .attr("cy", function(d) { return yScale(y(d)); })
          .attr("r", function(d) { return radiusScale(tamanho(d)); });
    }

    // Defines a sort order so that the smallest parties are drawn on top.
    function order(a, b) {
      return tamanho(b) - tamanho(a);
    }

    // After the transition finishes, you can mouseover to change the year.
    function enableInteraction() {
      var labelScale = d3.scale.linear()
          .domain([periodo_min, periodo_max])
          .range([l_box.x + 10, l_box.x + l_box.width - 10])
          .clamp(true);

      // Cancel the current transition, if any.
      svg.transition().duration(0);

      overlay
          .on("mouseover", mouseover_period)
          .on("mouseout", mouseout_period)
          .on("mousemove", mousemove_period)
          .on("touchmove", mousemove_period);

      function mouseover_period() {
        label.classed("active", true);
      }

      function mouseout_period() {
        label.classed("active", false);
      }

      function mousemove_period() {
        displayPeriod(labelScale.invert(d3.mouse(this)[0]));
      }
    }

    // Tweens the entire chart by first tweening the year, and then the data.
    // For the interpolated data, the parties and label are redrawn.
    function tweenYear() {
      var year = d3.interpolateNumber(periodo_min, periodo_max);
      return function(t) { displayPeriod(year(t)); };
    }

    function updatePartie(partie) {}
    
    // Updates the display to show the specified period.
    function displayPeriod(period) {
        var dados = interpolateData(period)
            .filter(function(d){ return d.tamanho;});
        
        var partie = svg.selectAll(".partie")
            .data(dados)
            .attr("transform", function(d) { return "translate(" + xScale(x(d)) +"," +  yScale(y(d)) + ")";});
        
        partie.enter()
          .append("circle")
            .attr("class", "partie_circle")
            .attr("id", function(d) { return "circle-" + nome(d); })
            .style("fill", function(d) { return gradiente(svg, nome(d), cor(d)); }) // colorScale(cor(d)); })
            .attr("r", function(d) { return radiusScale(tamanho(d)); });
    
        // Add a title.
        partie.enter()
          .append("title")
            .text(function(d) { return nome(d); });
   
        partie.enter()
          .append("text")
            .text(function(d){ return numero(d);})
                .attr("dx", "-8")
                .attr("dy", "3")

        //partie.sort(order)
        
        partie.exit().remove();
        //partie.data(dados, nome).call(position);
        //identification.data(dados, nome).call(position_text);
        label.text(periodos[Math.round(period)].nome);
        quantidade_votacoes = periodos[Math.round(period)].quantidade_votacoes
        total_label.text(quantidade_votacoes + " votações");
    }

    // Interpolates the dataset for the given (fractional) year.
    function interpolateData(year) {
      return partidos.map(function(d) {
              return {
                      nome: d.nome,
                      numero: d.numero,
                      cor: d.cor,
                      tamanho: interpolateValues(d.tamanho, year),
                      x: interpolateValues(d.x, year),
                      y: interpolateValues(d.y, year)
                    };
      });
    }

    // Finds (and possibly interpolates) the value for the specified year.
    function interpolateValues(values, year) {
      var i = bisect.left(values, year, 0, values.length - 1),
          a = values[i];
      if (i > 0) {
        var b = values[i - 1],
            t = (year - a[0]) / (b[0] - a[0]);
        return a[1] * (1 - t) + b[1] * t;
      }
      return a[1];
    }
  }

  return {
    initialize:initialize
  };
})(jQuery);
