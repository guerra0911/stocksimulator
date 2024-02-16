var socket = io.connect('http://localhost:5000');  // adjust as needed

var layout = {
    //title: 'Stock Price',
    xaxis: {
        title: 'Time',
        type: 'date'
    },
    yaxis: {
        title: 'Price'
    }
};

var config = {responsive: true};

socket.on('connect', function() {
    socket.emit('get_stock_data', dt1);  // replace 'AAPL' with your ticker
});


socket.on('new_stock_data', function(data) {
    var trace = {
        x: data.time,
        y: data.ohlc,
        mode: 'lines',
        type: 'scattergl',
        line: {color: 'rgb(75, 192, 192)'}
    };
    Plotly.newPlot('chart1', [trace], layout, config);
    Plotly.newPlot('chart2', [trace], layout, config);
    Plotly.newPlot('chart3', [trace], layout, config);
    Plotly.newPlot('chart4', [trace], layout, config);
});



