// Function to validate phone number format
function isValidPhoneNumber(phoneNumber) {
    // Add your validation logic here
    // For example, you can use regular expressions
    // Return true if valid, false otherwise
    return true;
}

// Function to validate email format
function isValidEmail(email) {
    // Add your validation logic here
    // Return true if valid, false otherwise
    return true;
}

// Function to handle cancel button click
function cancelChanges() {
    window.location.href = 'dashboard.html';
}

// Function to handle submit button click
function submitChanges() {
    var formData = new FormData(document.getElementById('editProfileForm'));

    // Use fetch API to send the form data to the Flask route
    fetch('/edit_profile', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Handle success (e.g., show a success message)
            alert(data.message);
        } else {
            // Handle failure (e.g., show an error message)
            alert('Failed to update profile: ' + data.error);
        }
    })
    .catch(error => console.error('Error submitting changes:', error));
}
