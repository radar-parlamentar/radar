d3.json("/static/files/codes/js/genero_comparativo_partidos.json", function(error, passa_dados) {

	legislatura = "2007-2011";
	dados = passa_dados[legislatura];
	data = [];
	for (key in dados) {
		elementos = {};
		elementos.State = key;
		elementos.feminino = dados[key].F;
		elementos.masculino = dados[key].M;
		data.push(elementos)
	}

	var margin = {top: 20, right: 100, bottom: 100, left: 60},
	    width = 960 - margin.left - margin.right,
	    height = 500 - margin.top - margin.bottom;

	var x = d3.scale.ordinal()
	    .rangeRoundBands([0, width], .1);

	var y = d3.scale.linear()
	    .rangeRound([height, 0]);

	var color = d3.scale.ordinal()
	    .range(["#98abc5", "#8a89a6", "#7b6888", "#6b486b", "#a05d56", "#d0743c", "#ff8c00"]);

	var xAxis = d3.svg.axis()
	    .scale(x)
	    .orient("bottom");

	var yAxis = d3.svg.axis()
	    .scale(y)
	    .orient("left")
	    .tickFormat(d3.format(".0%"));

	var svg = d3.select("#animacao").append("svg")
	    .attr("width", width + margin.left + margin.right)
	    .attr("height", height + margin.top + margin.bottom)
	  .append("g")
	    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  color.domain(d3.keys(data[0]).filter(function(key) {
	  if (key == "masculino" || key == "feminino") return true;
	  else return false;
	}));

  data.forEach(function(d) {
    var y0 = 0;
    d.ages = color.domain().map(function(name) { return {name: name, y0: y0, y1: y0 += +d[name]}; });
    d.ages.forEach(function(d) { d.y0 /= y0; d.y1 /= y0; });
  });

  data.sort(function(a, b) { return b.ages[0].y1 - a.ages[0].y1; });

  x.domain(data.map(function(d) { return d.State; }));

  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis)
		.selectAll("text")
		.style("text-anchor", "end")
		//.attr("dx", "-1.8em")
		//.attr("dy", ".5em")
		.attr("transform", function(d){ return "rotate(-45)"});

  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis);

	var tip = d3.tip()
	  .attr('class', 'd3-tip')
	  .offset([-10, 0])
	  .html(function(d) {
		  masc = parseInt(d.masculino);
		  feme = parseInt(d.feminino);
		  porcenM = Math.round((masc / (masc + feme))*10000)/100;
		  porcenF = Math.round((feme / (masc + feme))*10000)/100;
	    r = "<strong>Homens:</strong> <span style='color:yellow'>" + d.masculino + " ("+porcenM+"%)</span></br>";
	    r += "<strong>Mulheres:</strong> <span style='color:yellow'>" + d.feminino + " ("+porcenF+"%)</span></br>";
	    return r;
	  })

	svg.call(tip);

  var state = svg.selectAll(".state")
      .data(data)
    .enter().append("g")
      .attr("class", "state")
      .attr("transform", function(d) { return "translate(" + x(d.State) + ",0)"; })
	      .on('mouseover', tip.show)
	      .on('mouseout', tip.hide);

  state.selectAll("rect")
      .data(function(d) { return d.ages; })
    .enter().append("rect")
      .attr("width", x.rangeBand())
      .attr("y", function(d) { return y(d.y1); })
      .attr("class", function(d){return "barra-"+d.name;})
      .attr("height", function(d) { return y(d.y0) - y(d.y1); });

  var legend = svg.select(".state:last-child").selectAll(".legend")
      .data(function(d) { return d.ages; })
    .enter().append("g")
      .attr("class", "legend")
      .attr("transform", function(d) { return "translate(" + x.rangeBand() / 2 + "," + y((d.y0 + d.y1) / 2) + ")"; });

  legend.append("line")
      .attr("x2", 10);

  legend.append("text")
      .attr("x", 13)
      .attr("dy", ".35em")
      .text(function(d) { return d.name; });


});
