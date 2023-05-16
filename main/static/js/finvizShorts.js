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
                        let link = document.createElement('a');
                        link.setAttribute('target', '_blank');
                        link.setAttribute('href','https://www.tipranks.com/stocks/' + data[i][0] +
                            '/earnings');
                        link.className = 'link-offset-1 link-offset-2-hover link-underline link-underline-opacity-0 ' +
                            'link-underline-opacity-75-hover';
                        link.innerText = data[i][0];
                        cell.append(link);
                        cell.className = 'ps-2';
                        row.append(cell);
                        let cell_short_float = document.createElement('td');
                        cell_short_float.innerText = data[i][1];
                        cell_short_float.className = 'text-center';
                        row.append(cell_short_float);
                        let cell_short_ratio = document.createElement('td');
                        cell_short_ratio.innerText = data[i][2];
                        cell_short_ratio.className = 'text-center';
                        row.append(cell_short_ratio);
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