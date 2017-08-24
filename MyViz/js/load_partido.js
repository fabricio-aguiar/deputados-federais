var loadDsv = d3.dsv(";", "text / plain; charset = ISO - 8859 - 1");

loadDsv("data/Partidos-BR-Dados-Por-Periodo.csv", function (error, data) {
    if (error) {
        console.log(error);
    }
    
    d3.select('h2#data-title').text('Deputados federais');
    // d3.select('div#data pre')
    //     .html(JSON.stringify(data, null, 4)); 
    grafico(data);
    
})



grafico = function (data) {
    
var width = parseInt(d3.select('#graph')
    .style('width'), 10);
// console.log(width)

TRANS_DURATION = 2000;


// Getting our bar chart’ s dimensions
 var chartHolder = d3.select("#graph");

 var margin = {
     top: 20,
     right: 20,
     bottom: 30,
     left: 40
 };
 var boundingRect = chartHolder.node().getBoundingClientRect();
 var width = boundingRect.width - margin.left - margin.right,
     height = boundingRect.height - margin.top - margin.bottom;
 
 // SCALES WITH RANGES
 
 var xScale = d3.scale.ordinal()
 xScale.rangeBands([0, width], 0.1);

 var yScale = d3.scale.linear()
 yScale.rangeRound([height, 0]);
    
 
// AXES
var xAxis = d3.svg.axis()
    .scale(xScale)
    .orient("bottom");



var yAxis = d3.svg.axis()
    .scale(yScale)
    .orient('left')
    .ticks(10)
    .tickFormat(function (d) {
    //    if (nbviz.QtdPerCapita) {
    //         return d.toExponential();
    //     }
        return d;
    });

//tooltip
var tip = d3.tip()
        .attr('class', 'd3-tip')
        .offset([-10, 0])
        .html(function (data) {
            return "<strong>Total:</strong> <span style='color:red'>" + data.Qtd + "</span>";
        })

// build our chart’ s frame
 var svg = d3.select('#graph').append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g").classed('chart', true)
    .attr("transform", "translate(" + margin.left + "," +
        margin.top + ")");

svg.call(tip);

// ADD AXES
 svg.append("g")
     .attr("class", "x axis")
     .attr("transform", "translate(0," + height + ")");

 svg.append("g")
     .attr("class", "y axis")
     .append("text")
     .attr('id', 'y-axis-label')
     .attr("transform", "rotate(-90)")
     .attr("y", 6)
     .attr("dy", ".71em")
     .style("text-anchor", "end");


// OUR UPDATE FUNCTION
var update = function (data) {
        // A. Update scale domains with new data
        xScale.domain(data.map(function (d) { return d['Partido Atual']; }));
        yScale.domain([0, d3.max(data, function (d) {
            return +d.Qtd;
        })])};

update(data);

// B. Use the axes generators with the new scale domains
svg.select('.x.axis')
    .transition().duration(TRANS_DURATION)
    .call(xAxis) 
        .selectAll("text") 
            .style("text-anchor", "end")
            .attr("dx", "-.8em")
            .attr("dy", ".15em")
            .attr("transform", "rotate(-35)");

svg.select('.y.axis')
    .transition().duration(TRANS_DURATION)
    .call(yAxis);

var yLabel = svg.select('#y-axis-label');
yLabel.text("Numero de deputados");

 // JOIN DATA TO BAR-GROUP
 var bars = svg.selectAll('.bar')
     .data(data, function(d) {
        return d['Partido Atual']; 
    });
 // APPEND BARS FOR UNBOUND DATA
 bars.enter()
     .append('rect').classed('bar', true);
 // UPDATE ALL BARS WITH BOUND DATA
 bars.attr('height', function (d, i) {
     return height - yScale(d.Qtd);
 })
     .attr('width', xScale.rangeBand())
     .on('mouseover', tip.show)
     .on('mouseout', tip.hide)
     .transition().duration(TRANS_DURATION)
     .attr('y', function (d) {
         return yScale(d.Qtd);
     })
     .attr('x', function (d) { return xScale(d['Partido Atual']);  
     });
 // REMOVE ANY BARS WITHOUT BOUND DATA
 bars.exit().remove();

    }