document.addEventListener('DOMContentLoaded', () => {
    const uploadButton = document.getElementById('uploadButton');
    const fileInput = document.getElementById('fileInput');
    const uploadForm = document.getElementById('uploadForm');
    const fileDisplay = document.getElementById('fileDisplay');

    // Trigger file input when button is clicked
    uploadButton.addEventListener('click', () => {
        fileInput.click();
    });

    // Handle file selection
    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            // Display file name
            fileDisplay.textContent = fileInput.files[0].name;

            // Optionally show alert (optional - you can remove if unnecessary)
            alert("File selected: " + fileInput.files[0].name);

            // Submit form automatically
            uploadForm.submit();
        } else {
            fileDisplay.textContent = "No file selected";
        }
    });
});

// Optional: Show success alert manually if needed (can be triggered after form submission server response)
function showSuccessAlert() {
    alert("File cleaned successfully!");
}
