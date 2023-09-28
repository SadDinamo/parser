function getTipranksData(ticker) {
    // Ajax
    let s = new Date().toLocaleString();
    let result = null;
    $.ajax({
        url: 'http://localhost:8000/get_tipranks_data/' + ticker + '/',
        method: 'POST',
        dataType: 'json',
        data: {'ticker': ticker},
        headers: {"X-CSRFToken": getCookie('csrftoken')}, // mode: 'same-origin', // Do not send CSRF token to another domain.
        xhrFields: {withCredentials: true},
        success: function (data) {
            if (data) {
                let row = document.getElementById('short-' + ticker);
                let report_date = document.createElement('td');
                let reportDate = new Date(data['next_report_date']);
                let dateNow = new Date(Date.now());
                let diff = (reportDate.getTime() - dateNow.getTime()) / 1000 / 3600 / 24 + 1;
                if (diff < 15) {
                    document.getElementById('short-' + ticker + '-ticker').innerHTML =
                        document.getElementById('short-' + ticker + '-ticker').innerHTML +
                        '<span style="position:relative">' +
                        '<i class="bi bi-calendar text-danger-emphasis mx-1" ' +
                        'title="report to be published soon" style="position:absolute"></i>' +
                        '<span class="text-danger-emphasis" style="display:inline-block;' + 
			'text-align:center;font-size:75%;width: 1.33em;margin-top:0.3em;' + 
			'margin-left:0.33em">' +
                        + Math.floor(diff) + '</span>' +
                        '</span>'
                }
                report_date.innerText = data['next_report_date'];
                report_date.className = 'text-center';
                row.append(report_date);
                let consensus_eps = document.createElement('td');
                consensus_eps.innerText = data['consensus_eps_forecast'];
                consensus_eps.className = 'text-center';
                row.append(consensus_eps);
                let analyst_consensus = document.createElement('td');
                analyst_consensus.innerText = data['analyst_consensus'];
                analyst_consensus.className = 'text-center';
                row.append(analyst_consensus);
            } else {
                console.log(s + ": Unable to get data for getFinvizShorts")
            }
        },
        error: function (request, status, error) {
            console.log(s + ': Ajax error for getFinvizShorts: ' + request.response);
        },
    });
}

function getFinvizShorts() {
    // Ajax
    let s = new Date().toLocaleString();
    if (true) {
        $.ajax({
            url: '/get_top_shorts',
            method: 'POST',
            dataType: 'json',
            data: {},
            headers: {"X-CSRFToken": getCookie('csrftoken')},
            // mode: 'same-origin'
            // Do not send CSRF token to another domain
            success: function (data) {
                if (data) {
                    let tableBody = document.getElementById('top-shorts-table-body');
                    tableBody.innerHTML = '';
                    for (let i = 0; i < data.length; i++) {
                        let row = document.createElement('tr');
                        row.id = 'short-' + data[i][0];
                        let cell = document.createElement(`td`);
                        let link = document.createElement('a');
                        link.setAttribute('target', '_blank');
                        link.setAttribute('href', 'https://www.tipranks.com/stocks/' + data[i][0] +
                            '/earnings');
                        link.id = 'short-' + data[i][0] + '-ticker';
                        link.className = 'link-underline link-underline-opacity-0 d-flex flex-row';
                        link.innerText = data[i][0];
                        cell.append(link);
                        row.append(cell);
                        let cell_short_float = document.createElement('td');
                        cell_short_float.innerText = data[i][1];
                        cell_short_float.className = 'text-center';
                        row.append(cell_short_float);
                        tableBody.append(row);
                        getTipranksData(data[i][0]);
                    }
                } else {
                    console.log(s + ": Unable to get data for getFinvizShorts")
                }
                markFailToDeliver();
            },
            error: function (request, status, error) {
                console.log(s + ': Ajax error for getFinvizShorts: ' + request.response);
            },
        });
    }
}

function markFailToDeliver() {
    // Ajax
    let s = new Date().toLocaleString();
    if (true) {
        $.ajax({
            url: '/get_fail_to_deliver_list',
            method: 'POST',
            dataType: 'json',
            data: {},
            headers: {"X-CSRFToken": getCookie('csrftoken')}, // mode: 'same-origin', // Do not send CSRF token to another domain.
            success: function (data) {
                console.log(data);
                if (data) {
                    data.forEach(element => document.getElementById('short-' + element.toString() + '-ticker').innerHTML = document.getElementById('short-' + element.toString() + '-ticker').innerHTML + '<i class="bi bi-truck text-warning mx-1" title="failed-to-deliver"></i>');
                } else {
                    console.log(s + ": Unable to get fail to deliver list")
                }
            },
            error: function (request, status, error) {
                console.log(s + ': Ajax error for fail to deliver list: ' + xhr.status + ": " + xhr.responseText);
            },
        });
    }
}

getFinvizShorts();

let interval_getFinvizShorts = 1000 * 60 * 60; // refresh data every ... milliseconds
setInterval(() => {
    getFinvizShorts();
}, interval_getFinvizShorts); // milli sec

