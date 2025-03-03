    document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('fileInput');
    const fileNameInput = document.getElementById('fileNameInput');
    const uploadForm = document.getElementById('uploadForm');

    fileInput.addEventListener('change', function() {
        if (fileInput.files.length > 0) {
            // Display the file name in the textbox
            fileNameInput.value = fileInput.files[0].name;

            // Submit the form
            uploadForm.submit();
        } else {
            // Display message if no file is selected
            fileNameInput.value = 'No  selected';

            // Show a pop-up alert
            alert("Please select a file before submitting.");
            
            // Optional: Create a custom pop-up (instead of using alert)
            showCustomPopup("No file selected! Please choose a file.");
        }
    });

    // Function to create a custom pop-up
    function showCustomPopup(message) {
        let popup = document.createElement('div');
        popup.innerHTML = `<div style="
            position: fixed; 
            top: 50%; 
            left: 50%; 
            transform: translate(-50%, -50%);
            background: white; 
            padding: 20px; 
            border: 2px solid #ccc; 
            box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
            text-align: center;">
            <p>${message}</p>
            <button onclick="this.parentElement.remove()">OK</button>
        </div>`;
        document.body.appendChild(popup);
    }
});
