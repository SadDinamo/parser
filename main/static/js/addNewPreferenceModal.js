document.getElementById('showModalNewPreference').addEventListener('click', function () {
    var newPreferenceModal = new bootstrap.Modal(document.getElementById('createPreferenceModal'),
        {
            keyboard: false,
            backdrop: 'static'
        });
    newPreferenceModal.show();
})