(function (depviz) {
  
   
depviz.genero = function (gdata) {
    d3.select('#chart')
        .selectAll('svg').remove()
    var margin = { top: 10, right: 10, bottom: 10, left: 15 };
    var chartHolder = d3.select("#chart");
    var boundingRect = chartHolder.node().getBoundingClientRect();
    var width = boundingRect.width - margin.left - margin.right,
        height = boundingRect.height - margin.top - margin.bottom;
        // filtrando em masculino e feminino
        gdata.filter('MASCULINO');
        var homens = gdata.top(Infinity);

        gdata.filter();
        gdata.top(Infinity);

        gdata.filter('FEMININO');
        var mulheres = gdata.top(Infinity);

        h = homens.length;
        m = mulheres.length;
        dvs = 1;
        if (h > 100) {
            dvs = 10;
        }

    var sdata = [
        { 'n': h, 'color': '#0000FF', 'name': 'Homens', 'sex': 'male' }, 
        { 'n': m, 'color': '#8b0000', 'name': 'Mulheres', 'sex': 'female' },
    ];
        
    modulo = 20;
    
    var 
	xScale = d3.scale.linear()
	  .domain([0, modulo])
	  .range([0, width]),
	yScale = d3.scale.linear()
	  .domain([0, 8])
	  .range([height, 0]);
	 
	
	data = [];

    for (key in sdata) {
      for (i=0;i<sdata[key]['n'];i++) { 
          data.push({ 'sex': sdata[key]['sex'], 'color': sdata[key]['color'], 'total': sdata[key]['n']});
      }
    }

 count = 0;     
 modulo = modulo/2;
lh = Math.round(sdata[0]['n'] / dvs);
lm = Math.round(sdata[1]['n'] / dvs);
lt = lm + sdata[0]['n'];
for (key = 0; key < data.length; key++) {
    data[key]['x'] = -9;
    data[key]['y'] = 0;
}

 for (key = 0; key < lh; key++) {
   column = Math.floor(count/modulo);
   row = count % modulo;
   data[key]['x'] = row;
   data[key]['y'] = column;
   count++;
 }
//  altura = column;
 count=0;
 for (key = sdata[0]['n']; key < lt; key++) {
         column = Math.floor(count / modulo);
         row = count % modulo;
         data[key]['x'] = row + 10;
         data[key]['y'] = column;
         count++;
 }
//  if (altura < column){
//      altura = column;
//  }
//  icon = { 'width': height / 10, 'height': height / (altura + 2) };
 icon = { 'width': 18, 'height': 23 };


 var tip = d3.tip()
         .attr('class', 'd3-tip')
         .offset([-10, 0])
         .html(function (data) {
             return "<strong>Total:</strong> <span style='color:red'>" + data.total + "</span>";
         })

  var svg = d3.select("#chart").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  svg.call(tip);
    
  var icons = svg.selectAll(".icon")
		.data(data)
      .enter().append("text")
        .attr('font-family', 'FontAwesome')
        .attr('font-size', icon['height'])
        .attr('fill',function(d) {return d.color;})
        .attr('text-anchor',"middle")
        .attr('title',function(d) {return d.name;})
        .attr('x',function(d) {return xScale(d.x);})
        .attr('y',function(d) {return yScale(d.y);})
        .on('mouseover', tip.show)
        .on('mouseout', tip.hide)
        .attr("class",function (d) { if (d.sex == 'female') return 'mulher'; else return 'homem'; })
        .text(function(d) {if (d.sex == 'female') return '\uf182'; else return '\uf183'; });

    

 legend = ["Mulheres","Homens"];
 for (key in sdata) {        
  svg.append("text")
   .attr('font-size',18)
   .attr('font-family', 'sans-serif')
   .attr('text-anchor',"start")
   .attr('fill', sdata[key]['color'])
   .attr('x',function(d) {return key*width/2;})
   .attr('y',3)
   .text(sdata[key]['name']);
 }}
}(window.depviz = window.depviz || {}));