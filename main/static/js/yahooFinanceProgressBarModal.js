function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.getElementById('yahoo_parser_news-btn').addEventListener('click', function () {
    var myModal = new bootstrap.Modal(document.getElementById('yahooFinanceProgressBarModal'),
        {
            keyboard: false,
            backdrop: 'static'
        })
    myModal.show();
});

document.getElementById('yahoo_parser_news-btn').addEventListener('click', function () {
    let yahooInterval = setInterval(check_yahoo_finance_progress_bar, 1000);

    function check_yahoo_finance_progress_bar() {
        if (document.getElementById('yahooFinanceProgressBarModal').classList.contains('show')) {
            $.ajax({
                url: 'get_yahoo_ajax_progress_bar_data',
                method: 'POST',
                dataType: 'json',
                data: {'id': 'yahooFinanceProgressBar'},
                headers: {"X-CSRFToken": getCookie('csrftoken')},
                mode: 'same-origin', // Do not send CSRF token to another domain.
                success: function (data) {
                    let percent = (Math.round((data['current_ticker_counter'] / data['total_tickers']) * 100)).toString();
                    document.getElementById('yahooFinanceProgressBarLabel').innerText = percent + '% : ' + data['ticker_name'];
                    document.getElementById('yahooFinanceProgressBar').setAttribute('aria-valuenow', percent);
                    document.getElementById("yahooFinanceProgressBar").style.setProperty('width', percent + '%');
                },
                error: function () {
                    alert('Ajax error');
                },
            });
        }
    }
});
