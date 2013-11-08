function desenhar(legislatura){
	d3.json("/static/files/codes/js/genero_comparativo_partidos.json", function(error, passa_dados) {

		dados = passa_dados[legislatura];
		data = [];
		for (key in dados) {
			elementos = {};
			elementos.State = key;
			elementos.feminino = dados[key].F;
			elementos.masculino = dados[key].M;
			data.push(elementos)
		}

		var margin = {top: 20, right:30, bottom: 50, left: 50},
		    width = 900 - margin.left - margin.right,
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

        $("#loading").remove();
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

	 // var legend = svg.select(".state:last-child").selectAll(".legend")
	 //     .data(function(d) { return d.ages; })
	 //   .enter().append("g")
	 //     .attr("class", "legend")
	 //     .attr("transform", function(d) { return "translate(" + 2 * x.rangeBand() + "," + y(1 -  (d.y0 + d.y1)/3) + ")"; });

	 // legend.append("line")
	 //     .attr("wdith", 10)
	 //     .attr("height", 10)
	 //     .attr("class", function(d){ return "barra-"+d.name;});

	 // legend.append("text")
	 //     .attr("x", 13)
	 //     .attr("dy", ".35em")
	 //     .text(function(d) { return d.name; });

	});
}

desenhar("2011-2015");

legis = ['1864-1866', '1935-1937', '1967-1971', '1897-1899', '1983-1987', '1885-1885', '1845-1847', '1834-1837', '1971-1975', '1930-1930', '1975-1979', '1894-1896', '1934-1935', '1857-1860', '1906-1909', '1849-1852', '2007-2011', '1987-1991', '1946-1951', '1991-1995', '1979-1983', '1869-1872', '1903-1905', '1999-2003', '2003-2007', '1872-1875', '1853-1856', '2011-2015', '1900-1902', '1963-1967', '1867-1868', '1881-1884', '1927-1930', '1843-1844', '1912-1915', '1848-1848', '1830-1833', '1918-1921', '1951-1955', '1915-1918', '1924-1927', '1826-1829', '1959-1963', '1955-1959', '1995-1999', '1861-1863', '1878-1881', '1886-1889', '1891-1893', '1876-1877', '1838-1841', '1909-1912', '1921-1924']

$('.typeahead').typeahead({
	name: 'legislaturas',
	local: legis,
	limit: 10
}).on("typeahead:selected", function(obj, datum){
	$("#animacao").empty();
	desenhar(datum.value);
});


