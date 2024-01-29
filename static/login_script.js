function login() {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    // Send login credentials to the server for authentication
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
            // If authentication is successful, redirect to the dashboard
            window.location.href = '/dashboard';
        } else {
            alert('Invalid username or password. Please try again.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function goToForgotPassword() {
    window.location.href = 'forgot_password.html';
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

document.addEventListener('DOMContentLoaded', function () {
    var recoveryForm = document.getElementById('recoveryForm');

    recoveryForm.addEventListener('submit', function (event) {
        event.preventDefault();

        var email = document.getElementById('email').value;

        // Add logic to send recovery email
        sendRecoveryEmail(email);
    });

    function sendRecoveryEmail(email) {
        // Add AJAX or fetch request to send recovery email
        fetch('/process_recovery', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: email
            }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Password recovery email sent to ' + email);
            } else {
                alert('Failed to send recovery email. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
});
