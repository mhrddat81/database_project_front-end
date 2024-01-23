function login() {
    // Simple login logic
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    // You can replace this with your actual authentication logic
    if (username === 'demo' && password === 'password') {
        window.location.href = 'dashboard.html';
    } else if (username === null || password === null) {
        alert('Invalid username or password. Please try again.');
    }
    
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
