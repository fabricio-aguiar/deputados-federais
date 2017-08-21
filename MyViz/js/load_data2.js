var loadDsv = d3.dsv(";", "text / plain; charset = ISO - 8859 - 1");

loadDsv("data/Deputados-BR-Dados-Por-Periodo.csv", function (error, data) {
    if (error) {
        console.log(error);
    }
    
    d3.select('h2#data-title').text('Deputados federais do RJ');
    d3.select('div#data pre')
        .html(JSON.stringify(data, null, 4)); 
    makeFilterAndDimensions(data);
    
})

makeFilterAndDimensions = function (data) {
    filter = crossfilter(data);
    partidoDim = filter.dimension(function (o) {
        return o.Partido;
    })

    sexoDim = filter.dimension(function (o) {
        return o.Sexo;
    })
    
    partidoDim.filter('PMDB'); 
    var depPMDB = partidoDim.top(Infinity); 
    console.log("Numero de deputados do PMDB: " + depPMDB.length)
    for (i = 0; i < depPMDB.length; i++){
    console.log(depPMDB[i]["Nome Para Urna"])}

    partidoDim.filter();
    partidoDim.top(Infinity);

    grafico(sexoDim);
}

grafico = function (data) {
    
var width = parseInt(d3.select('#graph')
    .style('width'), 10);
console.log(width)

// Getting our bar chart’ s dimensions
var svg = d3.select('#graph').append("svg")

// filtrando em masculino e feminino
 data.filter('MASCULINO');
 var homens = data.top(Infinity);

 data.filter();
 data.top(Infinity);

 data.filter('FEMININO');
 var mulheres = data.top(Infinity);

//  criando objeto
var sexoData = [
    {key:'Homens', value: homens.length},
    {key:'Mulheres', value: mulheres.length}
];

// var barWidth = width / (sexoData.length * 2);

// sexoData.forEach(function (d, i) {
//     svg.append('rect').classed('bar', true)
//         .attr('height', d.value * 4)
//         .attr('width', barWidth)
//         .attr('y', height-(d.value * 4))
//         .attr('x', i*(barWidth));
// });

var bars = svg.selectAll('.bar')
    .data(sexoData);

bars = bars.enter();

bars.append('rect')
    .classed('bar', true)
    .attr('width', 20)
    .attr('height', function (d) { return d.value * 3.5; }) 
    .attr('x', function (d, i) { return (i+1) * 12; })
    .attr('name', function (d, i) {
        // Adicionando nome a cada barra do grafico, para facilitar sua manipulaçao depois
        var sane_key = d.key.replace(/ /g, '_'); 

        console.log('__data__ is: ' + JSON.stringify(d)
            + ', index is ' + i)

        return 'bar__' + sane_key; 
    });
};