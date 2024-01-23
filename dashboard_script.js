document.addEventListener("DOMContentLoaded", function() {
    // Sample function to handle menu item click
    var menuItems = document.querySelectorAll('.nav-link');
    menuItems.forEach(function(item) {
        item.addEventListener('click', function() {
            alert('Clicked: ' + item.textContent);
        });
    });

    // Sample function to load user profile data
    var profile = document.querySelector('.profile');
    profile.addEventListener('click', function() {
        // Assuming there's a function getUserProfileData() that fetches user data from the server
        var userData = getUserProfileData(); // You need to implement this function
        displayUserProfile(userData);
    });
});

function getUserProfileData() {
    // This is a placeholder function. You should implement it to fetch user data from your server.
    return {
        name: 'John Doe',
        profilePic: 'profile-pic.jpg',
        // Add more profile data as needed
    };
}

function displayUserProfile(userData) {
    var profileName = document.querySelector('.profile h4');
    var profilePic = document.querySelector('.profile img');

    // Update profile information in the right column
    profileName.textContent = userData.name;
    profilePic.src = userData.profilePic;

    // You can add more logic here to update additional profile information
}

document.addEventListener("DOMContentLoaded", function() {
    // Sample data for the transaction history chart
    var ctx = document.getElementById('transactionHistoryChart').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Transaction History',
                data: [],
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 2,
                fill: false
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    type: 'category',
                    position: 'bottom',
                    grid: {
                        display: false
                    }
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Amount'
                    }
                }
            }
        }
    });
});
