
d3.json("/static/files/codes/js/genero_base2.json", function(miserables) {
  var matrix = [],
      partidos = miserables.partidos,
      termos = miserables.termos,
      n_partidos = partidos.length,
      n_termos = termos.length,
      lista_partidos = [];

var margin = {top: 80, right: 0, bottom: 10, left: 80},
    width = 720,
    height = width / n_partidos * n_termos;

var x = d3.scale.ordinal().rangeBands([0, width]),
    z = d3.scale.pow().domain([5, 50]).clamp(true).nice(),
    c = d3.scale.category20().domain(d3.range(50));

    $("#loading").remove();

var svg = d3.select("#animacao").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .style("margin-left", -margin.left + "px")
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  // Compute index per node.
  termos.forEach(function(termo, i) {
	    matrix[i] = d3.range(n_partidos).map(function(j) { return {x: j, y: i, z: 0}; });
  });
  for (var chave in partidos) {
	  lista_partidos.push(partidos[chave].name);
  }
	  console.log(matrix);

  // Convert links to matrix; count character occurrences.
  miserables.links.forEach(function(link) {
    matrix[link.source][link.target].z += link.value;
    //matrix[link.target][link.source].z += link.value;
    //matrix[link.source][link.source].z += link.value;
    //matrix[link.target][link.target].z += link.value;
    //nodes[link.source].count += link.value;
    //nodes[link.target].count += link.value;
  });

  // Precompute the orders.
  //var orders = {
  //  name: d3.range(n).sort(function(a, b) { return d3.ascending(nodes[a].name, nodes[b].name); }),
  //  count: d3.range(n).sort(function(a, b) { return 0;}),//nodes[b].count - nodes[a].count; }),
  //  group: d3.range(n).sort(function(a, b) { return 0;})//nodes[b].group - nodes[a].group; })
  //};

  // The default sort order.
  //x.domain(orders.name);
  x.domain(lista_partidos);

  svg.append("rect")
      .attr("class", "matrix-background")
      .attr("width", width)
      .attr("height", height);

  var row = svg.selectAll(".row")
      .data(matrix)
    .enter().append("g")
      .attr("class", "row")
      .attr("transform", function(d, i) { return "translate(0," + x(i) + ")"; })
      .each(row);

  row.append("line")
      .attr("x2", width);

  row.append("text")
      .attr("x", -6)
      .attr("y", x.rangeBand() / 2)
      .attr("dy", ".32em")
      .attr("text-anchor", "end")
      .text(function(d, i) { return termos[i].name; });

  var column = svg.selectAll(".column")
      .data(partidos)
    .enter().append("g")
      .attr("class", "column")
      .attr("transform", function(d, i) { return "translate(" + x(i) + ")rotate(-90)"; });

  column.append("line")
      .attr("x1", -width);

  column.append("text")
      .attr("x", 6)
      .attr("y", x.rangeBand() / 2)
      .attr("dy", ".32em")
      .attr("text-anchor", "start")
      .text(function(d, i) { return partidos[i].name; });

  function row(row) {
    var cell = d3.select(this).selectAll(".cell")
        .data(row.filter(function(d) { return d.z; }))
      .enter().append("rect")
        .attr("class", "cell")
        .attr("x", function(d) { return x(d.x); })
        .attr("width", x.rangeBand())
        .attr("height", x.rangeBand())
        .style("fill-opacity", function(d) { return z(d.z); })
        .style("fill", function(d) { return 1; })
        .on("mouseover", mouseover)
        .on("mouseout", mouseout);
  }

  function mouseover(p) {
    d3.selectAll(".row text").classed("active", function(d, i) { return i == p.y; });
    d3.selectAll(".column text").classed("active", function(d, i) { return i == p.x; });
  }

  function mouseout() {
    d3.selectAll("text").classed("active", false);
  }

  //d3.select("#order").on("change", function() {
  //  clearTimeout(timeout);
  //  order(this.value);
  //});

  //function order(value) {
  //  x.domain(orders[value]);

  //  var t = svg.transition().duration(2500);

  //  t.selectAll(".row")
  //      .delay(function(d, i) { return x(i) * 4; })
  //      .attr("transform", function(d, i) { return "translate(0," + x(i) + ")"; })
  //    .selectAll(".cell")
  //      .delay(function(d) { return x(d.x) * 4; })
  //      .attr("x", function(d) { return x(d.x); });

  //  t.selectAll(".column")
  //      .delay(function(d, i) { return x(i) * 4; })
  //      .attr("transform", function(d, i) { return "translate(" + x(i) + ")rotate(-90)"; });
  //}

//  var timeout = setTimeout(function() {
//    order("group");
//    d3.select("#order").property("selectedIndex", 2).node().focus();
//  }, 5000);
});
