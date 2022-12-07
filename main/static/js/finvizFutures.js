function getFinvizFuturesData() {
    // Ajax
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
                    document.getElementById('tr-finviz-GC-name').innerText = data['GC']['label'];
                    document.getElementById('tr-finviz-GC-value').innerText = data['GC']['last'];
                    document.getElementById('tr-finviz-GC-change').innerText = data['GC']['change'];
                    document.getElementById('tr-finviz-GC-comment').innerText = '';

                    document.getElementById('tr-finviz-QA-name').innerText = data['QA']['label'];
                    document.getElementById('tr-finviz-QA-value').innerText = data['QA']['last'];
                    document.getElementById('tr-finviz-QA-change').innerText = data['QA']['change'];
                    document.getElementById('tr-finviz-QA-comment').innerText = '';

                    document.getElementById('tr-finviz-NQ-name').innerText = data['NQ']['label'];
                    document.getElementById('tr-finviz-NQ-value').innerText = data['NQ']['last'];
                    document.getElementById('tr-finviz-NQ-change').innerText = data['NQ']['change'];
                    document.getElementById('tr-finviz-NQ-comment').innerText = '';

                    document.getElementById('tr-finviz-NG-name').innerText = data['NG']['label'];
                    document.getElementById('tr-finviz-NG-value').innerText = data['NG']['last'];
                    document.getElementById('tr-finviz-NG-change').innerText = data['NG']['change'];
                    document.getElementById('tr-finviz-NG-comment').innerText = '';

                    document.getElementById('tr-finviz-ZW-name').innerText = data['ZW']['label'];
                    document.getElementById('tr-finviz-ZW-value').innerText = data['ZW']['last'];
                    document.getElementById('tr-finviz-ZW-change').innerText = data['ZW']['change'];
                    document.getElementById('tr-finviz-ZW-comment').innerText = '';

                    document.getElementById('tr-finviz-ES-name').innerText = data['ES']['label'];
                    document.getElementById('tr-finviz-ES-value').innerText = data['ES']['last'];
                    document.getElementById('tr-finviz-ES-change').innerText = data['ES']['change'];
                    document.getElementById('tr-finviz-ES-comment').innerText = '';

                    document.getElementById('tr-finviz-PL-name').innerText = data['PL']['label'];
                    document.getElementById('tr-finviz-PL-value').innerText = data['PL']['last'];
                    document.getElementById('tr-finviz-PL-change').innerText = data['PL']['change'];
                    document.getElementById('tr-finviz-PL-comment').innerText = '';

                    // add and show toast notification
                    let toasts = document.getElementById('toasts-section');
                    let toastHeader = document.createElement('div');
                    toastHeader.className = 'toast-header';
                    let toastHeaderText = document.createElement('strong');
                    toastHeaderText.className = 'me-auto';
                    toastHeaderText.innerText = 'Finviz futures';
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
                    toast.className = 'toast hide align-items-center border-0';
                    toast.setAttribute('role', 'alert');
                    toast.setAttribute('aria-live', 'assertive');
                    toast.setAttribute('aria-atomic', 'true');
                    toast.append(toastHeader);
                    toast.append(toastMessage);
                    toasts.append(toast);
                    let toastBs = new bootstrap.Toast(toast);
                    toastBs.show();
                    toastBs = null;
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