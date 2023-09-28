// import series from "../highcharts/code/es-modules/Core/Series/Series";

function getCnnFearAndGreedData() {
    // Ajax
    let s = new Date().toLocaleString();
    let toastDelay = 10000;
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
                    let greedLink = document.createElement('a');
                    greedLink.setAttribute('href', 'https://edition.cnn.com/markets/fear-and-greed');
                    greedLink.setAttribute('target', '_blank');
                    greedLink.innerText = 'CNN fear and greed index';
                    document.getElementById('cnn-fear-and-greed-name').innerHTML = '';
                    document.getElementById('cnn-fear-and-greed-name').append(greedLink);
                    document.getElementById("cnn-fear-and-greed-value").innerText =
                        '' + Math.round(data['fear_and_greed']['score']);
                    document.getElementById("cnn-fear-and-greed-change").innerText =
                        '' + Math.round((data['fear_and_greed']['score'] - data['fear_and_greed']['previous_close'])
                            * 10) / 100;
                    document.getElementById("cnn-fear-and-greed-comment").innerText =
                        '' + data['fear_and_greed']['rating'];

                    // add and show toast notification
                    let toasts = document.getElementById('toasts-section');
                    let toastHeader = document.createElement('div');
                    toastHeader.className = 'toast-header';
                    let toastHeaderText = document.createElement('strong');
                    toastHeaderText.className = 'me-auto';
                    toastHeaderText.innerText = 'Cnn fear and greed';
                    let toastMessage = document.createElement('div');
                    toastMessage.className = 'toast-body';
                    toastMessage.innerText = 'Data updated';
                    let toastButtonClose = document.createElement('button');
                    toastButtonClose.type = 'button';
                    toastButtonClose.className = 'btn-close me-2 m-auto';
                    toastButtonClose.setAttribute('data-bs-dismiss', 'toast');
                    toastButtonClose.setAttribute('aria-label', 'Close');
                    toastHeader.append(toastHeaderText, toastButtonClose);
                    let toast = document.createElement('div');
                    toast.className = 'toast hide align-items-center border-0 text-bg-success';
                    toast.setAttribute('role', 'alert');
                    toast.setAttribute('aria-live', 'assertive');
                    toast.setAttribute('aria-atomic', 'true');
                    toast.append(toastHeader);
                    toast.append(toastMessage);
                    toasts.append(toast);
                    let toastBs = new bootstrap.Toast(toast);
                    toastBs.delay = toastDelay;
                    toastBs.show();
                    toastBs = null;
                    setTimeout(() => {toast.remove(); toast = null; }, toastDelay + 1000);
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

let interval_cnnFearAndGreed = 1000 * 60 * 15; // refresh data every ... milliseconds
setInterval(() => {
    getCnnFearAndGreedData();
}, interval_cnnFearAndGreed); // milli sec