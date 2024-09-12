document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('id_file');
    const fileLabelText = document.getElementById('file-label-text');

    fileInput.addEventListener('change', function() {
        const fileName = fileInput.files[0] ? fileInput.files[0].name : 'No file chosen';
        fileLabelText.textContent = fileName;
    });
});
