// import series from "../highcharts/code/es-modules/Core/Series/Series";

Highcharts.chart('hc-fear-and-greed-container', {
    chart: {
        type: 'gauge',
        plotBackgroundColor: null,
        plotBackgroundImage: null,
        plotBorderWidth: 0,
        plotShadow: false,
        height: '45%'
    },
    title: {
        text: ''
    },
    credits: {
        enabled: false
    },
    tooltip: {
        enabled: false
    },
    navigation: {
        buttonOptions: {
            enabled: false
        }
    },
    pane: {
        startAngle: -90,
        endAngle: 90,
        background: null,
        center: ['50%', '100%'],
        size: '180%'
    },
    // the value axis
    yAxis: {
        min: 0,
        max: 100,
        tickPixelInterval: 100,
        tickPosition: 'inside',
        tickColor: Highcharts.defaultOptions.chart.backgroundColor || '#FFFFFF',
        tickLength: 30,
        tickWidth: 2,
        minorTickInterval: null,
        labels: {
            distance: 15,
            style: {
                fontSize: '14px'
            }
        },
        plotBands: [{
            from: 0,
            to: 25,
            color: '#F47378',
            thickness: 40
        }, {
            from: 25,
            to: 45,
            color: '#FBCFD0',
            thickness: 40
        }, {
            from: 45,
            to: 55,
            color: '#EDD3ED',
            thickness: 40
        }, {
            from: 55,
            to: 75,
            color: '#C8EFD4',
            thickness: 40
        }, {
            from: 75,
            to: 100,
            color: '#6BD089',
            thickness: 40
        }]
    },
    series: [{
        name: 'Fear and greed index',
        data: [0],
        dataLabels: {
            enabled: false,
            // format: '{y}',
            borderWidth: 0,
            color: (
                Highcharts.defaultOptions.title &&
                Highcharts.defaultOptions.title.style &&
                Highcharts.defaultOptions.title.style.color
            ) || '#333333',
            style: {
                fontSize: '16px'
            }
        },
        dial: {
            radius: '80%',
            backgroundColor: 'gray',
            baseWidth: 12,
            baseLength: '0%',
            rearLength: '0%'
        },
        pivot: {
            backgroundColor: 'gray',
            radius: 6
        }
    }]
});

function getCnnFearAndGreedData() {
    // Ajax
    const chart = Highcharts.charts[0];
    const point = chart.series[0].points[0];
    let newVal;
    let s = new Date().toLocaleString();
    if (true) {
        $.ajax({
            url: '/get_cnn_fear_and_greed_stats',
            method: 'POST',
            dataType: 'json',
            data: {},
            headers: {"X-CSRFToken": getCookie('csrftoken')},
            // mode: 'same-origin', // Do not send CSRF token to another domain.
            success: function (data) {
                if (data) {
                    newVal = data['fear_and_greed']['score'];
                    point.update(newVal);
                    document.getElementById('FnG-heading').innerText = 'CNN Fear and Greed index: ' +
                        Math.floor(data['fear_and_greed']['score']) + ' ' + data['fear_and_greed']['rating'];
                    // document.getElementById('yahooFinanceProgressBarLabel').innerText = percent + '% : ' + data['ticker_name'];
                    // document.getElementById('yahooFinanceProgressBar').setAttribute('aria-valuenow', percent);
                    // document.getElementById("yahooFinanceProgressBar").style.setProperty('width', percent + '%');
                } else {
                    console.log(s + ": Unable to get data for get_cnn_fear_and_greed_stats")
                }
            },
            error: function (request, status, error) {
                console.log(s + ': Ajax error for get_cnn_fear_and_greed_stats: ' + request.response);
            },
        });
    }
}

getCnnFearAndGreedData();

let interval_cnnFearAndGreed = 1000 * 60 * 5; // refresh data every ... milliseconds
setInterval(() => {
    getCnnFearAndGreedData();
}, interval_cnnFearAndGreed); // milli sec