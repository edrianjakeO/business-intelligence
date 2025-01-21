document.addEventListener('DOMContentLoaded', (event) => {
    const uploadButton = document.getElementById('uploadButton');
    const fileInput = document.getElementById('fileInput');
    const uploadForm = document.getElementById('uploadForm');
    const fileNameInput = document.getElementById('fileName');

    // When the button is clicked, trigger the file input dialog
    uploadButton.addEventListener('click', function() {
        fileInput.click();
    });

    // When a file is selected, automatically display the file name and submit the form
    fileInput.addEventListener('change', function() {
        if (fileInput.files.length > 0) {
            // Display the file name in the textbox
            fileNameInput.value = fileInput.files[0].name;

            // Submit the form
            uploadForm.submit();
        } else {
            // Display message if no file is selected
            fileNameInput.value = 'No file selected';
        }
    });
});


    function showAlert() {
        alert("File cleaned successfully!");
    }

