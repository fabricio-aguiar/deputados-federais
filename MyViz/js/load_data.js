(function (depviz) {
var loadDsv = d3.dsv(";", "text / plain; charset = ISO - 8859 - 1");

loadDsv("data/Deputados-BR-Dados-Por-Periodo.csv", function (error, data) {
    if (error) {
        console.log(error);
    }
    
    d3.select('h2#data-title').text('Deputados federais');
    // d3.select('div#data pre')
    //     .html(JSON.stringify(data, null, 4)); 
    depviz.data = data;
    depviz.makeFilterAndDimensions(data);
    depviz.genero(depviz.sexoDim);
})

depviz.makeFilterAndDimensions = function (data) {
    filter = crossfilter(data);
    depviz.partidoDim = filter.dimension(function (o) {
        return o.Partido;
    });

    depviz.sexoDim = filter.dimension(function (o) {
        return o.Sexo;
    });
    
    depviz.estadoDim = filter.dimension(function (o) {
        return o.UF;
    });
    // partidoDim.filter('PMDB'); 
    // var depPMDB = partidoDim.top(Infinity); 
    // console.log("Numero de deputados do PMDB: " + depPMDB.length)
    // for (i = 0; i < depPMDB.length; i++){
    // console.log(depPMDB[i]["Nome para Urna"])}

    // partidoDim.filter();
    // partidoDim.top(Infinity);

    // depviz.grafico(depviz.sexoDim);
    
}


    


depviz.grafico = function (data) {
    
var width = parseInt(d3.select('#graph')
    .style('width'), 10);
// console.log(width)

depviz.TRANS_DURATION = 2000;

// filtrando em masculino e feminino
data.filter('MASCULINO');
var homens = data.top(Infinity);

data.filter();
data.top(Infinity);

data.filter('FEMININO');
var mulheres = data.top(Infinity);

//  criando objeto
var sexoData = [
    { key: 'Homens', value: homens.length },
    { key: 'Mulheres', value: mulheres.length }
];


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
    //    if (nbviz.valuePerCapita) {
    //         return d.toExponential();
    //     }
        return d;
    });

//tooltip
var tip = d3.tip()
        .attr('class', 'd3-tip')
        .offset([-10, 0])
        .html(function (sexoData) {
            return "<strong>Total:</strong> <span style='color:red'>" + sexoData.value + "</span>";
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
        xScale.domain(data.map(function (d) { return d.key; }));
        yScale.domain([0, d3.max(data, function (d) {
            return +d.value;
        })])};

update(sexoData);

// B. Use the axes generators with the new scale domains
svg.select('.x.axis')
    .transition().duration(depviz.TRANS_DURATION)
    .call(xAxis) 
        .selectAll("text") 
            .style("text-anchor", "end")
            .attr("dx", "2em")  //.attr("dx", "-.8em")
            .attr("dy", "1em")// .attr("dy", ".15em")
            .attr("transform", "rotate(0)"); //.attr("transform", "rotate(-65)");

svg.select('.y.axis')
    .transition().duration(depviz.TRANS_DURATION)
    .call(yAxis);

var yLabel = svg.select('#y-axis-label');
yLabel.text("Numero de deputados");

 // JOIN DATA TO BAR-GROUP
 var bars = svg.selectAll('.bar')
     .data(sexoData, function(d) {
        return d.key; 
    });
 // APPEND BARS FOR UNBOUND DATA
 bars.enter()
     .append('rect').classed('bar', true);
 // UPDATE ALL BARS WITH BOUND DATA
 bars.attr('height', function (d, i) {
     return height - yScale(d.value);
 })
     .attr('width', xScale.rangeBand())
     .on('mouseover', tip.show)
     .on('mouseout', tip.hide)
     .transition().duration(depviz.TRANS_DURATION)
     .attr('y', function (d) {
         return yScale(d.value);
     })
     .attr('x', function (d) { return xScale(d.key);  
     });
 // REMOVE ANY BARS WITHOUT BOUND DATA
 bars.exit().remove();

}}(window.depviz = window.depviz || {}));