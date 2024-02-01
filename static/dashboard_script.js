document.addEventListener("DOMContentLoaded", function() {
    // ... (other code)

    // Fetch and display user profile data
    fetch('/dashboard', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ userid: 'your_user_id_here' }), // Replace with the actual user ID
    })
        .then(response => response.json())
        .then(data => {
            displayUserProfile(data.userinfo);
            displayTransactionHistory(data.transactioninfo);
        })
        .catch(error => console.error('Error fetching dashboard data:', error));

    // ... (other code)

    function displayUserProfile(userData) {
        var profileName = document.querySelector('.profile h4');
        var profilePic = document.querySelector('.profile img');

        // Update profile information in the right column
        profileName.textContent = userData.Username; // Update to the actual field names from your database
        // Assuming you have a field 'ProfilePic' in your database for the profile picture URL
        profilePic.src = userData.ProfilePic || 'default_profile_pic.jpg';
        // You can add more logic here to update additional profile information
    }

    function displayTransactionHistory(transactionHistoryData) {
        var transactionHistoryTableBody = document.querySelector('#transactionHistoryTableBody');
        // Clear existing rows
        transactionHistoryTableBody.innerHTML = '';

        // Create and append transaction history rows dynamically
        transactionHistoryData.forEach(function(transaction) {
            var row = document.createElement('tr');
            row.innerHTML = `
                <td>${transaction.PaidAmount}</td>
                <td>${transaction.BoughtAmount}</td>
                <td>${transaction.TransactionDate}</td>
                <td>${transaction.MarketName}</td>
            `;
            transactionHistoryTableBody.appendChild(row);
        });
    }

    function displayUserProfile(userData) {
        var profileName = document.querySelector('.profile h4');
        var profilePic = document.querySelector('.profile img');
    
        // Update profile information in the right column
        profileName.textContent = userData.firstName + ' ' + userData.lastName;
        profilePic.src = userData.profilePic;
    
        // You can add more logic here to update additional profile information
    }
});
