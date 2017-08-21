d3.json("data/uf.json", function (error, data) {
       
    
    active = d3.select(null);
    var featureCollection = topojson.feature(data, data.objects.uf);
    
    // DIMENSIONS AND SVG
    var mapContainer = d3.select('#dep-map');
    var boundingRect = mapContainer.node().getBoundingClientRect();
        width = boundingRect.width,
        height = boundingRect.height;

      
    var svg = mapContainer.append('svg')
        .attr("width", width)
        .attr("height", height);

    var bounds = d3.geo.bounds(featureCollection);
     tooltip = d3.select('#map-tooltip');

    var centerX = d3.sum(bounds, function (d) { return d[0]; }) / 2,
        centerY = d3.sum(bounds, function (d) { return d[1]; }) / 2;

    var projection = d3.geo.mercator()
        .scale(720)
        .center([centerX, centerY]);

    path = d3.geo.path()
        .projection(projection);

    svg.append("rect")
        .attr("class", "background")
        .attr("width", width)
        .attr("height", height)
        .on("click", reset);

     g = svg.append("g")
        .attr("class", "states")
        .selectAll("path")
        .data(featureCollection.features)
        .enter().append("path")
        .attr("d", path)
        .on("click", clicked);

    borda = svg.append("path")
        .attr("class", "state-borders")
        .attr("d", path(topojson.mesh(data, data.objects.uf, function (a, b) { return a !== b; })));

})

function clicked(d) {
  if (active.node() === this) return reset();
  active.classed("active", false);
  active = d3.select(this).classed("active", true);

  var bounds = path.bounds(d),
      dx = bounds[1][0] - bounds[0][0],
      dy = bounds[1][1] - bounds[0][1],
      x = (bounds[0][0] + bounds[1][0]) / 2,
      y = (bounds[0][1] + bounds[1][1]) / 2,
      scale = .9 / Math.max(dx / width, dy / height),
      translate = [width / 2 - scale * x, height / 2 - scale * y];
  
  
  g.transition()
      .duration(750)
      .style("stroke-width", 1.5 / scale + "px")
      .attr("transform", "translate(" + translate + ")scale(" + scale + ")");

  borda.transition()
      .duration(750)
      .style("stroke-width", 1.5 / scale + "px")
      .attr("transform", "translate(" + translate + ")scale(" + scale + ")");

  tooltip.select('h2').text(d.properties.name);
  px = "50%";
  py = "50%";

  if (d.id == "ES"){
        px = "20%";
        py = "50%";
  }
  
  setTimeout(function () { tooltip.style('top', (py)); }, 850);
  setTimeout(function () { tooltip.style('left', (px)); }, 850);
}

function reset() {
    active.classed("active", false);
    active = d3.select(null);

    g.transition()
        .duration(750)
        .style("stroke-width", "1.5px")
        .attr("transform", "");

    borda.transition()
        .duration(750)
        .style("stroke-width", "1.5px")
        .attr("transform", "");

    tooltip.style('left', '-9999px');
}

;