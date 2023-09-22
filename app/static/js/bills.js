// bills.js

// Function to add a new row for bill input
function addBillRow() {
	const tableBody = document.querySelector('.bills-table tbody');

	// Create a new row
	const newRow = document.createElement('tr');
	newRow.innerHTML = `
	    <td><input type="text" name="billName[]" placeholder="Enter bill name"></td>
	    <td><input type="number" name="billAmount[]" placeholder="Enter amount"></td>
	    <td><input type="date" name="billDueDate[]"></td>
	`;

	// Append the new row to the table
	tableBody.appendChild(newRow);
}

// Function to remove last row for bill input
function removeBillRow() {
	const tableBody = document.querySelector('.bills-table tbody');
	const lastRow = tableBody.lastElementChild;
	tableBody.removeChild(lastRow);
}

// Add a click event listener to the "Add" button
const addBillButton = document.getElementById('addBillButton');
if (addBillButton) {
	addBillButton.addEventListener('click', addBillRow);
}

// Add a click event listener to the "Remove" button
const removeBillButton = document.getElementById('removeBillButton');
if (removeBillButton) {
	removeBillButton.addEventListener('click', removeBillRow);
}
