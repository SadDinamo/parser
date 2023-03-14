function getFinvizCryptoData() {
    // Ajax
    let s = new Date().toLocaleString();
    if (true) {
        $.ajax({
            url: '/get_finviz_crypto_data',
            method: 'POST',
            dataType: 'json',
            data: {},
            headers: {"X-CSRFToken": getCookie('csrftoken')},
            // mode: 'same-origin', // Do not send CSRF token to another domain.
            success: function (data) {
                if (data) {
                    document.getElementById('tr-finviz-BTCUSD-name').innerHTML = '<i class="fa-solid fa-bitcoin-sign"></i>itcoin';
                    document.getElementById('tr-finviz-BTCUSD-value').innerText = data['BTCUSD']['last'];
                    document.getElementById('tr-finviz-BTCUSD-change').innerText = data['BTCUSD']['change'];
                    document.getElementById('tr-finviz-BTCUSD-comment').innerText = '';
                    // add and show toast notification
                    let toasts = document.getElementById('toasts-section');
                    let toastHeader = document.createElement('div');
                    toastHeader.className = 'toast-header';
                    let toastHeaderText = document.createElement('strong');
                    toastHeaderText.className = 'me-auto';
                    toastHeaderText.innerText = 'Finviz crypto';
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
                    console.log(s + ": Unable to get data for get_finviz_crypto_data")
                }
            },
            error: function (request, status, error) {
                console.log(s + ': Ajax error for get_finviz_crypto_data: ' + request.response);
            },
        });
    }
}

getFinvizCryptoData();


let interval_finvizCrypto = 1000 * 60 * 5; // refresh data every ... milliseconds
setInterval(() => {
    getFinvizCryptoData();
}, interval_finvizCrypto); // milli sec