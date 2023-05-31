function launchNewsUpdateBackground() {
    if (true) {
        $.ajax({
            url: '/launch_news_update_background',
            method: 'POST',
            dataType: 'json',
            data: {},
            headers: {"X-CSRFToken": getCookie('csrftoken')},
            // mode: 'same-origin', // Do not send CSRF token to another domain.
            success: function (data) {
            },
            error: function (request, status, error) {
                console.log(': Ajax error for launch_news_update_background: ' + xhr.status + ": " + xhr.responseText);
            },
        });
    }
}

function getNewsUpdateStatus() {
    // Ajax
    let s = new Date().toLocaleString();
    if (true) {
        $.ajax({
            url: '/get_news_update_status',
            method: 'POST',
            dataType: 'json',
            data: {},
            headers: {"X-CSRFToken": getCookie('csrftoken')},
            // mode: 'same-origin', // Do not send CSRF token to another domain.
            success: function (data) {
                if (data) {
                    if (data['yahoo_ticker_update']) {
                        document.getElementById('updating-news-wheel').classList.remove('d-none');
                        document.getElementById('updating-news-label').classList.remove('d-none');
                        document.getElementById('updating-news-rerun-button').classList.remove('d-none');
                        document.getElementById('updating-news-label').classList.add('d-inline');
                        document.getElementById('updating-news-label').innerText = 'News update ' +
                            data['current_ticker_counter'].toString() + ' of ' + data['total_tickers'].toString();
                        let percent = (Math.floor((data['current_ticker_counter'] / data['total_tickers']) * 100)).toString();
                        document.getElementById('updating-news-progressbar').setAttribute('aria-valuenow', percent);
                        document.getElementById("updating-news-progressbar").style.setProperty('width', percent + '%');
                    } else {
                        document.getElementById('updating-news-wheel').classList.add('d-none');
                        document.getElementById('updating-news-label').classList.remove('d-inline');
                        document.getElementById('updating-news-label').classList.add('d-none');
                        document.getElementById('updating-news-rerun-button').classList.add('d-none');
                        document.getElementById('updating-news-label').innerText = '';
                    }
                } else {
                    console.log(s + ": Unable to get data for get_news_update_status")
                }
            },
            error: function (request, status, error) {
                console.log(s + ': Ajax error for get_news_update_status: ' + xhr.status + ": " + xhr.responseText);
            },
        });
    }
}

function resetNewsUpdate() {
    // Ajax
    let s = new Date().toLocaleString();
    if (true) {
        $.ajax({
            url: '/reset_news_parser',
            method: 'POST',
            dataType: 'json',
            data: {},
            headers: {"X-CSRFToken": getCookie('csrftoken')},
            // mode: 'same-origin', // Do not send CSRF token to another domain.
            success: function (data) {
                if (data) {
                    console.log(s + ': ' + data);
                    launchNewsUpdateBackground();
                } else {
                    console.log(s + ": Unable to reset news update status")
                }
            },
            error: function (request, status, error) {
                console.log(s + ': Ajax error for reset news update status: ' + xhr.status + ": " + xhr.responseText);
            },
        });
    }
}

document.getElementById('updating-news-rerun-button').addEventListener('click', resetNewsUpdate);
launchNewsUpdateBackground();

let interval_launchNewsUpdateBackground = 1000 * 60 * 30; // refresh data every ... milliseconds
setInterval(() => {
    getNewsUpdateStatus();
}, interval_launchNewsUpdateBackground); // milli sec

let interval_getNewsUpdateStatus = 1000 * 5; // refresh data every ... milliseconds
setInterval(() => {
    getNewsUpdateStatus();
}, interval_getNewsUpdateStatus); // milli sec