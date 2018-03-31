
d3.csv("/static/files/codes/js/genero_historia_base.csv", function(error, data) {

	var margin = {top: 20, right: 30, bottom: 50, left: 50},
	    width = 900 - margin.left - margin.right,
	    height = 500 - margin.top - margin.bottom;

	//anos = ["1826","1900","1950","2000", "2011"];
	anos = [];
	pula = true;
	data.forEach(function(d) {
		if (pula) anos.push(d.Ano);
		pula = !pula;
	});

	var x = d3.time.scale().range([0, width]);

	var y = d3.scale.linear()
	    .rangeRound([height, 0]);

	var color = d3.scale.ordinal()
	    .range(["#850000", "#aaaaaa", "#7b6888", "#6b486b", "#a05d56", "#d0743c", "#ff8c00"]);

    $("#loading").remove();
    
	var xAxis = d3.svg.axis()
	    .scale(x)
	    .orient("bottom")
	    //.tickFormat(d3.time.format("%Y"))
	    .tickFormat(function(d){return d;})
		.tickValues(anos)
//#.ticks(d3.time.years, 4);

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
	  if (key == "Masculino" || key == "Feminino") return true;
	  else return false;
  }));

  data.forEach(function(d) {
    var y0 = 0;
    d.ages = color.domain().map(function(name) { return {name: name, y0: y0, y1: y0 += +d[name], dur: d["Duracao"]}; });
    d.ages.forEach(function(d) { d.y0 /= y0; d.y1 /= y0; });
  });

  data.sort(function(a, b) { return b.ages[0].y1 - a.ages[0].y1; });

//x.domain(data.map(function(d) { return d.Ano; }));
	x.domain(d3.extent(data, function(d) { return d.Ano; }));

  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis)
      	.selectAll("text")
	.style("text-anchor", "end")
	//.attr("dx", "-1.8em")
	//.attr("dy", ".5em")
	.attr("transform", function(d){ return "rotate(-45)"})
      ;

  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis);

var tip = d3.tip()
  .attr('class', 'd3-tip')
  .offset([-10, 0])
  .html(function(d) {
	  masc = parseInt(d.Masculino);
	  feme = parseInt(d.Feminino);
	  porcenM = Math.round((masc / (masc + feme))*10000)/100;
	  porcenF = Math.round((feme / (masc + feme))*10000)/100;
    r = "<strong>Legislatura:</strong> <span style='color:yellow'>"  + d.Legislatura + "</span></br>";
    r += "<strong>Homens:</strong> <span style='color:yellow'>" + d.Masculino + " ("+porcenM+"%)</span></br>";
    r += "<strong>Mulheres:</strong> <span style='color:yellow'>" + d.Feminino + " ("+porcenF+"%)</span></br>";
    return r;
  })

svg.call(tip);

  var state = svg.selectAll(".state")
      .data(data)
    .enter().append("g")
      .attr("class", "state")
      .attr("transform", function(d) { return "translate(" + x(d.Ano) + ",0)"; })
       .on('mouseover', tip.show)
      .on('mouseout', tip.hide);

  state.selectAll("rect")
      .data(function(d) { return d.ages; })
    .enter().append("rect")
      .attr("x", x.range()[0])
      .attr("class", function(d){return "barra"+d.name;})
      .attr("width", function(d){return (parseInt(d.dur))*4;})
      .attr("y", function(d) { return y(d.y1); })
      .attr("height", function(d) { return y(d.y0) - y(d.y1); });
      //.style("fill", function(d) { return color(d.name); });


//  var legend = svg.select(".state:last-child").selectAll(".legend")
//      .data(function(d) { return d.ages; })
//    .enter().append("g")
//      .attr("class", "legend")
//      .attr("transform", function(d) { return "translate(" + x.range() / 2 + "," + y((d.y0 + d.y1) / 2) + ")"; });
//
//  legend.append("line")
//      .attr("x2", 10);
//
//  legend.append("text")
//      .attr("x", 13)
//      .attr("dy", ".35em")
//      .text(function(d) { return d.name; });

});
