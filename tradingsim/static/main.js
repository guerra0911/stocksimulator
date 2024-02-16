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
    console.log('Connected')
    for (var i = 1; i <= 4; i++) {
        document.getElementById('spinner' + i).style.display = 'block';  // Show the spinners
    }
    socket.emit('get_stock_data', dt1, dt2, dt3, dt4); 
});

socket.on('new_stock_data', function(data_list) {
    for (var i = 0; i < data_list.length; i++) {
        document.getElementById('spinner' + (i + 1)).style.display = 'none';  // Hide the spinners
        var data = data_list[i];
        var trace = {
            x: data.time,
            y: data.ohlc,
            mode: 'lines',
            type: 'scattergl',
            line: {color: 'rgb(75, 192, 192)'}
        };
        Plotly.newPlot('chart' + (i + 1), [trace], layout, config);
    }
});