var margin = {top: 40, right: 10, bottom: 10, left: 10},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

var color = d3.scale.category20c();

var treemapF = d3.layout.treemap()
    .size([width, height])
    .sticky(true)
    .value(function(d) { return d.size; });

var treemapM = d3.layout.treemap()
    .size([width, height])
    .sticky(true)
    .value(function(d) { return d.size; });

d3.json("/static/files/codes/js/genero_treemap_mulheres.json", function(error, root) {
    $("#loading").remove();
    var divF = d3.select("#mulheres").append("div")
        .style("position", "relative")
        .style("width", (width + margin.left + margin.right) + "px")
        .style("height", (height + margin.top + margin.bottom) + "px")
        .style("left", margin.left + "px")
        .style("top", margin.top + "px");

    var nodeF = divF.datum(root).selectAll(".nodeF")
        .data(treemapF.nodes)
      .enter().append("div")
        .attr("class", "nodeF")
        .call(position)
        .style("background", "#850000")//function(d) { return d.children ? color(d.name) : null; })
        .style("color", "#ffffff")
        .text(function(d) { return d.name + " - " + d.size;});//return d.children ? null : d.name; });

      nodeF
          .data(treemap.value(function(d) { return d.size; }).nodes)
        .transition()
          .duration(1500)
          .call(position);

  });

d3.json("/static/files/codes/js/genero_treemap_homens.json", function(error, root) {
    $("#loading").remove();
    var divM = d3.select("#homens").append("div")
        .style("position", "relative")
        .style("width", (width + margin.left + margin.right) + "px")
        .style("height", (height + margin.top + margin.bottom) + "px")
        .style("left", margin.left + "px")
        .style("top", margin.top + "px");

    var nodeM = divM.datum(root).selectAll(".nodeM")
        .data(treemapM.nodes)
      .enter().append("div")
        .attr("class", "nodeM")
        .call(position)
        .style("background", function(d) { return d.children ? color(d.name) : null; })
        .text(function(d) { return d.name + " - " + d.size;});//return d.children ? null : d.name; });

      nodeM
          .data(treemap.value(function(d) { return d.size; }).nodes)
        .transition()
          .duration(1500)
          .call(position);
  });

    $("#loading").remove();

function position() {
  this.style("left", function(d) { return d.x + "px"; })
      .style("top", function(d) { return d.y + "px"; })
      .style("width", function(d) { return Math.max(0, d.dx - 1) + "px"; })
      .style("height", function(d) { return Math.max(0, d.dy - 1) + "px"; });
}
