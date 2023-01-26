
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
                console.log(s + ': Ajax error for launch_news_update_background: ' + xhr.status + ": " + xhr.responseText);
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
                    if (data['yahoo_ticker_update']){
                        document.getElementById('updating-news-wheel').classList.remove('d-none');
                        document.getElementById('updating-news-label').classList.remove('d-none');
                        document.getElementById('updating-news-label').innerText = 'News update ' +
                            data['current_ticker_counter'].toString() + ' of ' + data['total_tickers'].toString();
                    } else {
                        document.getElementById('updating-news-wheel').classList.add('d-none');
                        document.getElementById('updating-news-label').classList.add('d-none');
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

launchNewsUpdateBackground();

let interval_launchNewsUpdateBackground = 1000 * 60 * 30; // refresh data every ... milliseconds
setInterval(() => {
    getNewsUpdateStatus();
}, interval_launchNewsUpdateBackground); // milli sec

let interval_getNewsUpdateStatus = 1000 * 5; // refresh data every ... milliseconds
setInterval(() => {
    getNewsUpdateStatus();
}, interval_getNewsUpdateStatus); // milli sec