(function (depviz) {    
    // depviz.listardep(depviz.data);
          

 depviz.listardep = function (data) {
    var rows, cells, upd;
    // Sort the winners' data by year
    var data = data.sort(function (a, b) {
        return +b['Total CEAP'] - +a['Total CEAP']; 
    });
    upd = d3.select('#dep-list tbody')
        .selectAll('tr').remove()
    // Bind our winner's data to the table rows
    rows = d3.select('#dep-list tbody')
        // .selectAll('tr').remove()
        .selectAll('tr')
        .data(data);

    rows.enter().append('tr') 
        .on('click', function (d) {
            console.log('You clicked a row ' + JSON.stringify(d));
            d3.select('div#data pre')
                .html(JSON.stringify(d, null, 4)); 
            window.scrollBy(0, 880);
            // displayDep(d); 
        });
    // Fade out excess rows over 2 seconds
    TRANS_DURATION = 2000;
    rows.exit()
        .transition().duration(TRANS_DURATION)
        .style('opacity', 0)
        .remove();
    
    // aux = data;
    // aux.forEach(function(d) {
    //   d['Total CEAP'] = "R$ " + d['Total CEAP'];
    //   d['Total CEAP'] = d['Total CEAP'].replace(".",",");  
    // });
    
    var localized = d3.locale({
        "decimal": ",",
        "thousands": ".",
        "grouping": [3],
        "currency": ["R$", ""],
        "dateTime": "%d/%m/%Y %H:%M:%S",
        "date": "%d/%m/%Y",
        "time": "%H:%M:%S",
        "periods": ["AM", "PM"],
        "days": ["Domingo", "Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"],
        "shortDays": ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"],
        "months": ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"],
        "shortMonths": ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
    });
    var numberFormat = localized.numberFormat(",.2f");
    
    var formatDecimalComma = d3.format(".2f"),
        formatMoney = function (d) { return "R$ " + numberFormat(formatDecimalComma(d)); };

    cells = rows.selectAll('td') 
        .data(function (d) {
            return [d['Nome para Urna'], formatMoney(d['Total CEAP']), d.Partido, d.UF, numberFormat(d['Atuacao em meses'])];
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
}(window.depviz = window.depviz || {}));