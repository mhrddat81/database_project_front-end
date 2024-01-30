
const authenticateURL = '/authenticate';

function login() {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    fetch('/authenticate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username: username,
            password: password,
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = '/dashboard';  // Redirect on successful login
        } else {
            alert('Invalid username or password. Please try again.');
        }
    })
    .catch(error => {
        console.error('Error during authentication:', error);
        alert('An error occurred during authentication. Please try again.');
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
