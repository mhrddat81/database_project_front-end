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

document.addEventListener("DOMContentLoaded", function () {
    // Sample dynamic asset data (replace with actual data fetching logic)
    var assetsData = [
        { name: 'Asset 1', value: 1000 },
        { name: 'Asset 2', value: 500 },
        // Add more assets as needed
    ];

    // Sample dynamic transaction history data (replace with actual data fetching logic)
    var transactionHistoryData = [
        { transaction: 'dollar', amount: 200,status: 'buy', total: 1200, date: '2022-03-01', time: '14:30' },
        { transaction: 'IR Toman', amount: 100000000, status:'sell', total: 1100, date: '2022-03-02', time: '10:45' },
        // Add more transaction history entries as needed
    ];

    // Create and append asset tiles dynamically
    var assetRow = document.getElementById('asset-row');
    assetsData.forEach(function (asset) {
        var col = document.createElement('div');
        col.className = 'col-md-3';
        col.innerHTML = `
            <div class="asset-tile bg-light p-3 text-center">
                <h5>${asset.name}</h5>
                <p>$${asset.value}</p>
            </div>
        `;
        assetRow.appendChild(col);
    });

    // Create and append transaction history rows dynamically
    var transactionHistoryTableBody = document.querySelector('tbody');
    transactionHistoryData.forEach(function (transaction) {
        var row = document.createElement('tr');
        row.innerHTML = `
            <td>${transaction.transaction}</td>
            <td>${transaction.amount}</td>
            <td>${transaction.status}</td>
            <td>${transaction.total}</td>
            <td>${transaction.date}</td>
            <td>${transaction.time}</td>
        `;
        transactionHistoryTableBody.appendChild(row);
    });

    // Continue with the rest of your JavaScript code for the chart
});

