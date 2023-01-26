
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
                    // for (let i = 0; i < data.length; i++) {
                    //     let card_wrapper = document.createElement('div');
                    //     card_wrapper.className = 'col-lg-3 col-sm-6 px-0 py-1';
                    //     document.getElementById("top-news-section").append(card_wrapper);
                    //
                    //     let card_link = document.createElement('a');
                    //     card_link.className = 'small text-decoration-none';
                    //     card_link.setAttribute('href', data[i].link);
                    //     card_link.setAttribute('target', '_blank');
                    //     //card_link.innerText = 'read the source';
                    //     card_wrapper.append(card_link);
                    //
                    //     let card_div = document.createElement('div');
                    //     card_div.className = 'card mx-1 h-100';
                    //     card_link.append(card_div);
                    //
                    //     let card_header = document.createElement('div');
                    //     card_header.className = 'card-header h-100 border-bottom-0';
                    //     card_div.append(card_header);
                    //
                    //     let card_header_h = document.createElement('h6');
                    //     card_header_h.className = 'small';
                    //     card_header_h.innerText = data[i].title;
                    //     card_header.append(card_header_h);
                    //
                    //     //let card_body = document.createElement('div');
                    //     //card_body.className = 'card-body';
                    //     //card_div.append(card_body);
                    //
                    //     //let card_text = document.createElement('p');
                    //     //card_text.className = 'card-text';
                    //     //card_text.innerText = data[i].description;
                    //     //card_body.append(card_text);
                    //
                    //     let card_footer = document.createElement('div');
                    //     card_footer.className = 'card-footer py-1 px-2';
                    //     card_div.append(card_footer);
                    //
                    //     let card_date = document.createElement('p');
                    //     let card_date_text = data[i].pubDate.replace(/T/g, ' ');
                    //     card_date_text = card_date_text.replace(/Z/g, '');
                    //     card_date.innerText = card_date_text;
                    //     card_date.className = 'small mb-0';
                    //     card_footer.append(card_date);
                    // };
                    // document.getElementById("top-news-section").innerText = data
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

let interval_launchNewsUpdateBackground = 1000 * 60 * 60; // refresh data every ... milliseconds
setInterval(() => {
    getNewsUpdateStatus();
}, interval_launchNewsUpdateBackground); // milli sec

let interval_getNewsUpdateStatus = 1000 * 5; // refresh data every ... milliseconds
setInterval(() => {
    getNewsUpdateStatus();
}, interval_getNewsUpdateStatus); // milli sec