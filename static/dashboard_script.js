document.addEventListener("DOMContentLoaded", function() {
    // Sample function to handle menu item click
    var menuItems = document.querySelectorAll('.nav-link');
    menuItems.forEach(function(item) {
        item.addEventListener('click', function() {
            alert('Clicked: ' + item.textContent);
        });
    });

    // Fetch and display user profile data
    fetch('/get_user_profile_data')  // Update this endpoint to match your Flask route
        .then(response => response.json())
        .then(data => displayUserProfile(data))
        .catch(error => console.error('Error fetching user profile data:', error));

    // Fetch and display dynamic asset data
    fetch('/get_assets_data')  // Update this endpoint to match your Flask route
        .then(response => response.json())
        .then(data => displayDynamicAssets(data))
        .catch(error => console.error('Error fetching dynamic asset data:', error));

    // Fetch and display transaction history data
    fetch('/get_transaction_history_data')  // Update this endpoint to match your Flask route
        .then(response => response.json())
        .then(data => displayTransactionHistory(data))
        .catch(error => console.error('Error fetching transaction history data:', error));
});

function displayUserProfile(userData) {
    var profileName = document.querySelector('.profile h4');
    var profilePic = document.querySelector('.profile img');

    // Update profile information in the right column
    profileName.textContent = userData.name;
    profilePic.src = userData.profilePic;

    // You can add more logic here to update additional profile information
}

function displayDynamicAssets(assetsData) {
    var assetRow = document.getElementById('asset-row');

    // Create and append asset tiles dynamically
    assetsData.forEach(function(asset) {
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
}

function displayTransactionHistory(transactionHistoryData) {
    var transactionHistoryTableBody = document.querySelector('tbody');

    // Create and append transaction history rows dynamically
    transactionHistoryData.forEach(function(transaction) {
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
}
