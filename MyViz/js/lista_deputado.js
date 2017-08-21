var loadDsv = d3.dsv(";", "text / plain; charset = ISO - 8859 - 1");

loadDsv("data/Deputados-BR-Dados-Por-Periodo.csv", function (error, data) {
    if (error) {
        console.log(error);
    }
    
    listardep(data);
          
})

listardep = function (data) {
    var rows, cells;
    // // Sort the winners' data by year
    // var data = data.sort(function (a, b) {
    //     return +b.year - +a.year;
    // });
    // Bind our winner's data to the table rows
    rows = d3.select('#dep-list tbody')
        .selectAll('tr')
        .data(data);

    rows.enter().append('tr') 
        .on('click', function (d) {
            console.log('You clicked a row ' + JSON.stringify(d));
            d3.select('div#data pre')
                .html(JSON.stringify(d, null, 4)); 
            // displayDep(d); 
        });
    // Fade out excess rows over 2 seconds
    TRANS_DURATION = 2000;
    rows.exit()
        .transition().duration(TRANS_DURATION)
        .style('opacity', 0)
        .remove();
    
    data.forEach(function(d) {
      d['Total CEAP'] = "R$ " + d['Total CEAP'];
      d['Total CEAP'] = d['Total CEAP'].replace(".",",");  
    });

    cells = rows.selectAll('td') 
        .data(function (d) {
            return [d['Nome para Urna'], d['Total CEAP'], d.Partido, d.UF, d['Atuacao em meses']];
        });

    // Append data cells, then set their property text
    cells = cells.enter().append('td');
    cells.text(function (d) {
        return d;
    });

    // Display a random winner if there is one or more
    // if (data.length) {
    //     displayDep(
    //         data[Math.floor(Math.random() * data.length)]); 
    // }
}
;