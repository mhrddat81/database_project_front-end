// Sample dynamic currency data (replace with actual data fetching logic)
var currencyData = [
    { currency: 'USD', price: 1.00 },
    { currency: 'EUR', price: 0.85 },
    { currency: 'GBP', price: 0.73 },
    { currency: 'IRR', price: 0.01 },
    { currency: 'TRL', price: 0.24 },
    { currency: 'BTC', price: 10}
    // Add more currencies as needed
];

var walletData = {
    'IR Rial': 1000,
    'US Dollar': 1000,
    'TRL': 1000,
    'Bitcoin': 10,
};
// Function to dynamically create and populate the currency dropdown
function populateCurrencyDropdown() {
    var currencySelects = document.querySelectorAll('.currency-select');

    currencySelects.forEach(function (currencySelect) {
        currencyData.forEach(function (currency) {
            var option = document.createElement('option');
            option.value = currency.currency;
            option.textContent = currency.currency;
            currencySelect.appendChild(option);
        });
    });
}

// Function to add a new row to the table
function addRow() {
    var currencyTableBody = document.getElementById('currencyTableBody');

    var newRow = document.createElement('tr');
    newRow.innerHTML = `
        <td>
            <select class="form-control currency-select">
                <!-- Currencies will be dynamically added here -->
            </select>
        </td>
        <td><input type="number" class="form-control amount-input" placeholder="Enter Amount" min="0"></td>
        <td>
            <select class="form-control" id="buySellSelect">
                <option value="buy">Buy</option>
                <option value="sell">Sell</option>
            </select>
        </td>
        <td><span class="price">0</span></td>
        <td><button type="button" class="btn btn-danger" onclick="removeRow(this)">Remove</button></td>
    `;

    currencyTableBody.appendChild(newRow);
    // Update the currency dropdown for the new row
    populateCurrencyDropdown();
}

// Function to remove a row from the table
function removeRow(button) {
    var row = button.parentNode.parentNode;
    row.parentNode.removeChild(row);
}

// Function to update the price based on the selected currency and amount
function updatePrice(row) {
    var currencySelect = row.cells[0].getElementsByTagName('select')[0];
    var amountInput = row.cells[1].getElementsByTagName('input')[0];
    var priceSpan = row.cells[3].getElementsByClassName('price')[0];

    var selectedCurrency = currencySelect.value;
    var amount = parseFloat(amountInput.value);

    if (!isNaN(amount) && amount >= 0) {
        var currency = currencyData.find(c => c.currency === selectedCurrency);
        if (currency) {
            var price = currency.price * amount;
            priceSpan.textContent = price.toFixed(2);
        }
    }
}

// Function to handle changes in the amount or currency dropdown
function handleRowChange(row) {
    updatePrice(row);
}

// Function to handle trade cancellation
function cancelTrade() {
    // Implement logic for cancelling the trade and redirecting to the dashboard
    window.location.href = 'dashboard.html';
}

// Function to handle trade button click
function submitPurchase() {
    // Implement logic for submitting the purchase and updating the wallet amount
    // ...

    // Update wallet amount after the trade (replace with actual data fetching logic)
    updateWalletAmount();

    // Update transaction history in the dashboard window
    updateTransactionHistory();

    // Show a success message or handle the result accordingly
    alert('Purchase submitted successfully!');
}

// Execute functions when the document is ready
document.addEventListener("DOMContentLoaded", function () {
    // Populate the currency dropdown
    populateCurrencyDropdown();
    
    // Add event listeners for dynamic updates
    var currencyTableBody = document.getElementById('currencyTableBody');
    currencyTableBody.addEventListener('change', function (event) {
        var target = event.target;
        if (target.tagName === 'SELECT' || target.tagName === 'INPUT') {
            var row = target.closest('tr');
            handleRowChange(row);
        }
    });
});
