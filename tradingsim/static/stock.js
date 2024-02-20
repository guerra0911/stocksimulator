var socket = io.connect('http://localhost:5000');  // adjust as needed

function formatDate(date) {
    var d = new Date(date),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear();

    if (month.length < 2) 
        month = '0' + month;
    if (day.length < 2) 
        day = '0' + day;

    return [year, month, day].join('-');
}

var now = new Date();

var fiveYearsAgo = new Date();
fiveYearsAgo.setFullYear(now.getFullYear() - 5);

var oneYearAgo = new Date();
oneYearAgo.setFullYear(now.getFullYear() - 1);

var nineMonthsAgo = new Date();
nineMonthsAgo.setMonth(now.getMonth() - 9);

var sixMonthsAgo = new Date();
sixMonthsAgo.setMonth(now.getMonth() - 6);

var threeMonthsAgo = new Date();
threeMonthsAgo.setMonth(now.getMonth() - 3);

var oneMonthAgo = new Date();
oneMonthAgo.setMonth(now.getMonth() - 1);

var fiveDaysAgo = new Date();
fiveDaysAgo.setDate(now.getDate() - 5);

var oneDayAgo = new Date();
oneDayAgo.setDate(now.getDate() - 1);


function createLayout(allTime, now) {
    //Calculate the number of years of data
    var yearsOfData = now.getFullYear() - new Date(allTime).getFullYear();

    //Create the buttons array
    var buttons = [
        {
            args: ['xaxis.range', [allTime, formatDate(now)]],
            label: 'MAX',
            method: 'relayout'
        }
    ];

    //Conditionally add buttons based on the number of years of data
    if (yearsOfData >= 5) {
        buttons.push({
            args: ['xaxis.range', [formatDate(fiveYearsAgo), formatDate(now)]],
            label: '5Y',
            method: 'relayout'
        });
    }
    if (yearsOfData >= 1) {
        buttons.push({
            args: ['xaxis.range', [formatDate(oneYearAgo), formatDate(now)]],
            label: '1Y',
            method: 'relayout'
        });
    }
    buttons.push({
        args: ['xaxis.range', [formatDate(nineMonthsAgo), formatDate(now)]],
        label: '9M',
        method: 'relayout'
    });
    buttons.push({
        args: ['xaxis.range', [formatDate(sixMonthsAgo), formatDate(now)]],
        label: '6M',
        method: 'relayout'
    });
    buttons.push({
        args: ['xaxis.range', [formatDate(threeMonthsAgo), formatDate(now)]],
        label: '3M',
        method: 'relayout'
    });
    buttons.push({
        args: ['xaxis.range', [formatDate(oneMonthAgo), formatDate(now)]],
        label: '1M',
        method: 'relayout'
    });
    buttons.push({
        args: ['xaxis.range', [formatDate(fiveDaysAgo), formatDate(now)]],
        label: '5D',
        method: 'relayout'
    });
    buttons.push({
        args: ['xaxis.range', [formatDate(oneDayAgo), formatDate(now)]],
        label: '1D',
        method: 'relayout'
    });
    
    return {
        xaxis: {
            title: 'Time',
            type: 'date'
        },

        yaxis: {
            title: 'Price'
        },

        margin: {
            l: 60,  // left margin
            r: 20,  // right margin
            t: 75,  // top margin
            b: 60   // bottom margin
        },

        updatemenus: [
            {
                buttons: buttons,
                direction: 'left',
                pad: {'r': 0, 't': 0},
                showactive: true,
                type: 'buttons',
                x: 0.86,
                xanchor: 'right',
                y: 1.15,
                yanchor: 'top'
            }
        ]
    };
}

var config = {responsive: true};

socket.on('connect', function() {
    console.log('Connected')
    document.getElementById('spinner').style.display = 'block';  // Show the spinner
    socket.emit('get_ind_stock_data', ind_stock); 
});

socket.on('new_ind_stock_data', function(data_dict) {
    var now = new Date();
    // No need to use a loop for one data
    document.getElementById('spinner').style.display = 'none';  // Hide the spinner
    var data = data_dict;
    var trace = {
        x: data.time,
        y: data.ohlc,
        mode: 'lines',
        type: 'scattergl',
        line: {color: 'rgb(75, 192, 192)'}
    };

    // Create a new layout for the chart
    var allTime = formatDate(new Date(data.time[0]));  // assuming data.time is sorted in ascending order
    var layout = createLayout(allTime, now);

    Plotly.newPlot('chart', [trace], layout, config);
});
