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
    
    var firstName = document.getElementById('firstName').value;
    var lastName = document.getElementById('lastName').value;
    var email = document.getElementById('email').value;
    var phoneNumber = document.getElementById('phoneNumber').value;
    var dob = document.getElementById('dob').value;

    // Validate phone number format
    if (!isValidPhoneNumber(phoneNumber)) {
        alert('Invalid phone number format!');
        return;
    }

    // Validate email format
    if (!isValidEmail(email)) {
        alert('Invalid email format!');
        return;
    }

    // Add additional validation for other fields as needed

    // Implement logic to submit changes to the database
    // ...

    // Show the updated information
    alert('Changes submitted successfully!');
}
