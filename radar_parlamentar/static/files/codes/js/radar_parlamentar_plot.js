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
  
  // Chart dimensions.
  var margin = {top: 19.5, right: 100, bottom: 19.5, left: 39.5},
      width = 880 - margin.right - margin.left;
      height = 590 - margin.top - margin.bottom;
  
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
    
    var periodo_min = 1,
        periodo_max = 2,
        first_label = "1o sem. 1788";
    
    // Create the SVG container and set the origin.
    var svg = d3.select("#animacao").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .style("position", "relative")
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    
    var partidos = dados.partidos,
        periodos = dados.periodos,
        list_partds = []
        list_periodos = [];
    
    //Carregando os períodos extremos dos dados
    
    periodo_min = d3.min( [ (parseInt(index)+1) for (index in d3.keys(periodos)) ] );
    periodo_max = d3.max( [ (parseInt(index)+1) for (index in d3.keys(periodos)) ] );

    first_label = periodos[periodo_min].nome;
    first_total = periodos[periodo_min].quantidade_votacoes + " votações";

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
        .text("Votações analisadas no período: " + first_total)
    
    // A bisector since many nation's data is sparsely-defined.
    var bisect = d3.bisector(function(d) { return d[0]; });

    // Add a dot per nation. Initialize the data at 1800, and set the colors.
    var dot = svg.append("g")
        .attr("class", "dots")
      .selectAll(".dot")
        .data(interpolateData(1))
      .enter().append("circle")
        .attr("class", "dot")
        .style("fill", function(d) { return colorScale(cor(d)); })
        .call(position)
        .sort(order);

    // Add a title.
    dot.append("title")
        .text(function(d) { return nome(d); });

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
  
    // Positions the dots based on data.
    function position(dot) {
      dot .attr("cx", function(d) { return xScale(x(d)); })
          .attr("cy", function(d) { return yScale(y(d)); })
          .attr("r", function(d) { return radiusScale(tamanho(d)); });
    }

    // Defines a sort order so that the smallest dots are drawn on top.
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
          .on("mouseover", mouseover)
          .on("mouseout", mouseout)
          .on("mousemove", mousemove)
          .on("touchmove", mousemove);

      function mouseover() {
        label.classed("active", true);
      }

      function mouseout() {
        label.classed("active", false);
      }

      function mousemove() {
        displayYear(labelScale.invert(d3.mouse(this)[0]));
      }
    }

    // Tweens the entire chart by first tweening the year, and then the data.
    // For the interpolated data, the dots and label are redrawn.
    function tweenYear() {
      var year = d3.interpolateNumber(periodo_min, periodo_max);
      return function(t) { displayYear(year(t)); };
    }

    // Updates the display to show the specified year.
    function displayYear(year) {
      dot.data(interpolateData(year), nome).call(position).sort(order);
      label.text(periodos[Math.round(year)].nome);
      quantidade_votacoes = periodos[Math.round(year)].quantidade_votacoes
      total_label.text(quantidade_votacoes + " votações");
    }

    // Interpolates the dataset for the given (fractional) year.
    function interpolateData(year) {
      return partidos.map(function(d) {
        return {
          nome: d.nome,
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
