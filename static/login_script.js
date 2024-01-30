function login() {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    // Prepare data to send in the AJAX request
    var requestData = {
        username: username,
        password: password
    };

    // Make an AJAX request to the Flask server
    $.ajax({
        type: 'POST',
        url: '/authenticate',
        contentType: 'application/json;charset=UTF-8',
        data: JSON.stringify(requestData),
        success: function(response) {
            if (response.success) {
                // Authentication success, redirect to the dashboard
                window.location.href = 'dashboard.html';
            } else {
                // Authentication failed, show an alert or handle accordingly
                alert('Authentication failed. Invalid username or password.');
            }
        },
        error: function(error) {
            // Handle any error that occurs during the AJAX request
            console.error('Error during authentication:', error.responseText);
        }
    });
}

function goToForgotPassword() {
    window.location.href = 'forgot-password.html';
}

function sendRecoveryEmail() {
    var email = document.getElementById('email').value;
    // Add logic to send recovery email
    alert('Password recovery email sent to ' + email);
}

function goToLogin() {
    window.location.href = 'login.html';
}

function register() {
    var newUsername = document.getElementById('newUsername').value;
    var newPassword = document.getElementById('newPassword').value;
    // Add logic to handle user registration
    alert('User registered!\nUsername: ' + newUsername + '\nPassword: ' + newPassword);
}
