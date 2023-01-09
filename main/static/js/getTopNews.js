// import series from "../highcharts/code/es-modules/Core/Series/Series";

function getTopNews(NewsCount) {
    // Ajax
    let s = new Date().toLocaleString();
    if (true) {
        $.ajax({
            url: '/get_top_news',
            method: 'POST',
            dataType: 'json',
            data: {'newsCount': NewsCount},
            headers: {"X-CSRFToken": getCookie('csrftoken')},
            // mode: 'same-origin', // Do not send CSRF token to another domain.
            success: function (data) {
                if (data) {
                    console.log(data);
                    for (let i = 0; i < data.length; i++) {
                        let card_wrapper = document.createElement('div');
                        card_wrapper.className = 'col-lg-3 col-sm-6 px-0 py-1';
                        document.getElementById("top-news-section").append(card_wrapper);
                        let card_div = document.createElement('div');
                        card_div.className = 'card mx-1 h-100';
                        card_wrapper.append(card_div);
                        let card_header = document.createElement('div');
                        card_header.className = 'card-header';
                        let card_header_h = document.createElement('h6');
                        card_header_h.innerText = data[i].title;
                        card_header.append(card_header_h);
                        card_div.append(card_header);
                        let card_body = document.createElement('div');
                        card_body.className = 'card-body';
                        card_div.append(card_body);
                        let card_text = document.createElement('p');
                        card_text.className = 'card-text';
                        card_text.innerText = data[i].description;
                        card_body.append(card_text);
                        let card_footer = document.createElement('div');
                        card_footer.className = 'card-footer';
                        card_div.append(card_footer);
                        let card_link = document.createElement('a');
                        card_link.className = 'small';
                        card_link.setAttribute('href', data[i].link);
                        card_link.setAttribute('target', '_blank');
                        card_link.innerText = 'read the source';
                        card_footer.append(card_link);
                    }
                    ;
                    // document.getElementById("top-news-section").innerText = data
                } else {
                    console.log(s + ": Unable to get data for get_top_news")
                }
            },
            error: function (request, status, error) {
                console.log(s + ': Ajax error for get_top_news: ' + xhr.status + ": " + xhr.responseText);
            },
        });
    }
}

getTopNews(20);

let interval_getTopNews = 1000 * 60 * 1; // refresh data every ... milliseconds
setInterval(() => {
    getTopNews(20);
}, interval_getTopNews); // milli sec