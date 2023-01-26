document.getElementById('yahoo_parser_news_show-btn').addEventListener('click', function () {
    var myModal = new bootstrap.Modal(document.getElementById('yahooFinanceProgressBarModal'),
        {
            keyboard: false,
            backdrop: 'static'
        })
    myModal.show();
});

document.getElementById('yahoo_parser_news_show-btn').addEventListener('click', function () {
    let yahooInterval = setInterval(check_yahoo_finance_progress_bar, 1000);

    function check_yahoo_finance_progress_bar() {
        if (document.getElementById('yahooFinanceProgressBarModal').classList.contains('show')) {
            $.ajax({
                url: '/get_yahoo_ajax_progress_bar_data',
                method: 'POST',
                dataType: 'json',
                data: {},
                headers: {"X-CSRFToken": getCookie('csrftoken')},
                mode: 'same-origin', // Do not send CSRF token to another domain.
                success: function (data) {
                    if (data['yahoo_ticker_update']) {
                        let percent = (Math.floor((data['current_ticker_counter'] / data['total_tickers']) * 100)).toString();
                        document.getElementById('yahooFinanceProgressBarLabel').innerText = percent + '% : ' + data['ticker_name'];
                        document.getElementById('progress-bar').setAttribute('aria-valuenow', percent);
                        document.getElementById("progress-bar").style.setProperty('width', percent + '%');
                    } else {
                        document.getElementById('yahooFinanceProgressBarLabel').innerText = '';
                        document.getElementById('yahooFinanceProgressBar').setAttribute('aria-valuenow', 0);
                        document.getElementById("yahooFinanceProgressBar").style.setProperty('width', 0 + '%');
                    }
                    document.getElementById("check-send-email-notifications").disabled = data['yahoo_ticker_update'];
                    document.getElementById("yahoo_parser_news-btn").disabled = data['yahoo_ticker_update'];
                    document.getElementById("news-parser-email-input").disabled = data['yahoo_ticker_update'];
                },
                error: function () {
                    alert('Ajax error');
                },
            });
        }
    }
});
