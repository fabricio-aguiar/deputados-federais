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
            // console.log('You clicked a row ' + JSON.stringify(d));
            // d3.select('div#data')
            //     .html(JSON.stringify(d, null, 4)); 
            displayDep(d); 
            document.getElementById('dados-dep').scrollIntoView();
            window.scrollBy(-900, 0);
            // window.scrollBy(0, 880);
            // window.scrollTo(0, document.body.scrollHeight);
        });
    // Fade out excess rows over 2 seconds
    TRANS_DURATION = 2000;
    rows.exit()
        .transition().duration(TRANS_DURATION)
        .style('opacity', 0)
        .remove();
    
      
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
            return [d['Nome para Urna'], d['Situacao na Legislatura Atual'], formatMoney(d['Total CEAP']), d.Partido, d.UF, Math.floor(d['Atuacao em meses'])];
        });

    // Append data cells, then set their property text
    cells = cells.enter().append('td');
    cells.text(function (d) {
        return d;
    });

    
    displayDep = function (data) {
        link = "http://inter01.tse.jus.br/divulga-cand-2014/eleicao/2014/idEleicao/143/cargo/6/UF/";
        link = link + data.UF + "/candidato/";
        d3.select('div#data')
          .selectAll('*')
          .remove();
        d3.select('div#data')
          .append('img') 
          .attr('src', data['foto']) 
          .attr("class", "foto");
        d3.select('div#data')
            .append('div')
            .attr("id", "dados-dep")
            .attr("class", "lado");

        direita = d3.select('.lado');

             direita.append('strong')
                    .append('p')
                    .text(data['Nome para Urna']);

             direita.append('p')
                 .text("Bens: " + formatMoney(data.Bens));
             
             id = data['foto'].split("/")[9];
             id = id.split(".")[0];
             direita.append('a')
                 .attr('href', link + id)
                 .text("Veja mais ");
                 
        }
            
    
 }
}(window.depviz = window.depviz || {}));