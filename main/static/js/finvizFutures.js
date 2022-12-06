function getFinvizFuturesData() {
    // Ajax
    const chart = Highcharts.charts[0];
    const point = chart.series[0].points[0];
    let newVal;
    let s = new Date().toLocaleString();
    if (true) {
        $.ajax({
            url: '/get_finviz_futures_data',
            method: 'POST',
            dataType: 'json',
            data: {},
            headers: {"X-CSRFToken": getCookie('csrftoken')},
            // mode: 'same-origin', // Do not send CSRF token to another domain.
            success: function (data) {
                if (data) {
                    document.getElementById('finvizFuturesGold').innerText = data['GC']['label'] +
                        " " + data['GC']['last'] + " " + data['GC']['change'] + "%";
                    document.getElementById('finvizFuturesBrent').innerText = data['QA']['label'] +
                        " " + data['QA']['last'] + " " + data['QA']['change'] + "%";
                    document.getElementById('finvizNasdaq100').innerText = data['NQ']['label'] +
                        " " + data['NQ']['last'] + " " + data['NQ']['change'] + "%";
                    document.getElementById('finvizNaturalGas').innerText = data['NG']['label'] +
                        " " + data['NG']['last'] + " " + data['NG']['change'] + "%";
                    // console.log(data);
                } else {
                    console.log(s + ": Unable to get data for get_finviz_futures_data")
                }
            },
            error: function (request, status, error) {
                console.log(s + ': Ajax error for get_finviz_futures_data: ' + request.response);
            },
        });
    }
}

getFinvizFuturesData();


let interval_finvizFutures = 1000 * 60 * 5; // refresh data every ... milliseconds
setInterval(() => {
    getFinvizFuturesData();
}, interval_finvizFutures); // milli sec