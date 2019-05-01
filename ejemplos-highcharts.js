		$(function () {
		    $.getJSON('{{ url_for('dashboard.datajson', id=lugar['id'], sensor=3) }}', function (data) {
		        // Crea el grafico con el id del lugar
		        $('#{{lugar['name']}}').highcharts('StockChart', {
		            rangeSelector : {
		                selected : 2
		            },
		            title : {
		                text : '{{lugar['name']}}'
		            },
		            series : [{
		                name : '{{sensor}}',
		                data : [[1554487190000.0, 21.9], [1554487180000.0, 22.9], [1554487170000.0, 23.9], [1554487160000.0, 25.9], [1554487150000.0, 24.9], [1554487140000.0, 23.9]],
		                tooltip: {
		                    valueDecimals: 2
		                }
                             }, //End Serie 1
                             {
                                name : '{{sensor}}',
                                data : [[1554487190000.0, 48.0], [1554487180000.0, 50.0], [1554487170000.0, 65.0], [1554487160000.0, 70.0], [1554487150000.0, 60.0], [1554487140000.0, 50.0]],
                                tooltip: {
                                    valueDecimals: 2
                                }                               
		            }] //End Series array
		        });//End o container.highcharts()
		    });//End of funtion (data)
		}); //End o function ()





$(function() {

    // If you need to specify any global settings such as colors or other settings you can do that here

    // Build Chart A
    $('#chart-A').highcharts({
        chart: {
            type: 'column'
        },
        title: {
            text: 'Chart A'
        },
        xAxis: {
            categories: ['Jane', 'John', 'Joe', 'Jack', 'jim']
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Apple Consumption'
            }
        },
        legend: {
            enabled: false
        },
        credits: {
            enabled: false
        },
        tooltip: {
            shared: true
        },
        series: [{
            name: 'Apples',
            data: [5, 3, 8, 2, 4]            
        }]
    });

    // Build Chart B
    $('#chart-B').highcharts({
        chart: {
            type: 'column'
        },
        title: {
            text: 'Chart B'
        },
        xAxis: {
            categories: ['Jane', 'John', 'Joe', 'Jack', 'jim']
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Miles during Run'
            }
        },
        legend: {
            enabled: false
        },
        credits: {
            enabled: false
        },
        tooltip: {
            shared: true
        },
        series: [{
            name: 'Miles',
            data: [2.4, 3.8, 6.1, 5.3, 4.1]
        }]
    });
});














var seriesOptions = [],
    seriesCounter = 0,
    names = ['MSFT', 'AAPL', 'GOOG'];

/**
 * Create the chart when all data is loaded
 * @returns {undefined}
 */
function createChart() {

    Highcharts.stockChart('container', {

        rangeSelector: {
            selected: 4
        },

        yAxis: {
            labels: {
                formatter: function () {
                    return (this.value > 0 ? ' + ' : '') + this.value + '%';
                }
            },
            plotLines: [{
                value: 0,
                width: 2,
                color: 'silver'
            }]
        },

        plotOptions: {
            series: {
                compare: 'percent',
                showInNavigator: true
            }
        },

        tooltip: {
            pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b> ({point.change}%)<br/>',
            valueDecimals: 2,
            split: true
        },

        series: seriesOptions
    });
}

$.each(names, function (i, name) {

    $.getJSON('https://www.highcharts.com/samples/data/' + name.toLowerCase() + '-c.json',    function (data) {

        seriesOptions[i] = {
            name: name,
            data: data
        };

        // As we're loading the data asynchronously, we don't know what order it will arrive. So
        // we keep a counter and create the chart when all the data is loaded.
        seriesCounter += 1;

        if (seriesCounter === names.length) {
            createChart();
        }
    });
});



$(function() {

    Highcharts.setOptions({
        global: {
            useUTC: false
        }
    });

    // Create the chart
    window.chart = new Highcharts.StockChart({
        chart: {
            renderTo: 'container',
            events: {
                load: function() {

                    // set up the updating of the chart each second
                    var series = this.series;
                    setInterval(function() {
                        for (var i = 0; i < series.length-1; i++) {
                            
                            var x = (new Date()).getTime(),
                                // current time
                                y = Math.round(Math.random() * 100);
                            series[i].addPoint([x, y], true, true);
                        
                        }
                    }, 1000);
                }
            }
        },

        rangeSelector: {
            buttons: [{
                count: 1,
                type: 'minute',
                text: '1M'},
            {
                count: 5,
                type: 'minute',
                text: '5M'},
            {
                type: 'all',
                text: 'All'}],
            inputEnabled: false,
            selected: 0
        },

        title: {
            text: 'Live random data'
        },

        exporting: {
            enabled: false
        },

        series: [{
            name: 'Random data',
            data: (function() {
                // generate an array of random data
                var data = [],
                    time = (new Date()).getTime(),
                    i;

                for (i = -999; i <= 0; i++) {
                    data.push([
                        time + i * 1000,
                        Math.round(Math.random() * 100)
                        ]);
                }
                return data;
            })()},
        {
            name: 'Random data2',
            data: (function() {
                // generate an array of random data
                var data = [],
                    time = (new Date()).getTime(),
                    i;

                for (i = -999; i <= 0; i++) {
                    data.push([
                        time + i * 1000,
                        Math.round(Math.random() * 100)
                        ]);
                }
                return data;
            })()

            }]
    });

});




(function() {
                // generate an array of random data
                return data;
            })()
