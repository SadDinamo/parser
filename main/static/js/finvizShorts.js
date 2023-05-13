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
            // mode: 'same-origin', // Do not send CSRF token to another domain.
            success: function (data) {
                if (data) {
                    let tableBody = document.getElementById('top-shorts-table-body');
                    tableBody.innerHTML = '';
                    for (let i = 0; i < data.length; i++) {
                        let row = document.createElement('tr');
                        let cell = document.createElement(`td`);
                        cell.className = 'py-0';
                        let link = document.createElement('a');
                        link.setAttribute('target', '_blank');
                        link.setAttribute('href','https://www.tipranks.com/stocks/' + data[i] +
                            '/earnings');
                        link.innerText = data[i];
                        cell.append(link);
                        row.append(cell);
                        tableBody.append(row);
                    }
                } else {
                    console.log(s + ": Unable to get data for getFinvizShorts")
                }
            },
            error: function (request, status, error) {
                console.log(s + ': Ajax error for getFinvizShorts: ' + request.response);
            },
        });
    }
}

getFinvizShorts();

let interval_getFinvizShorts = 1000 * 60 * 60; // refresh data every ... milliseconds
setInterval(() => {
    getFinvizShorts();
}, interval_getFinvizShorts); // milli sec