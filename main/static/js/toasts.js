//  Show all Django messages as bootstrap toasts after html loaded
$(document).ready(function () {
    let toasts = document.getElementsByClassName('toast');
    for (let i = 0; i < toasts.length; ++i) {
        let toast = new bootstrap.Toast(toasts[i]);
        toast.show();
        toast = null;
    }
});