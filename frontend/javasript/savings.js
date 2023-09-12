// savings.js

// Function to create a new savings plan
function createSavingsPlan() {
	// Get form input values
	const planName = document.getElementById('planName').value;
	const monthlyContribution = document.getElementById('monthlyContribution').value;
	const dueDate = document.getElementById('dueDate').value;
	const duration = document.getElementById('duration').value;

	// Validate input values (you can add more validation as needed)
	if (!planName || !monthlyContribution || !dueDate || !duration) {
		alert('Please fill in all fields.');
		return;
	}

	// Create a new savings plan object (you can define your own data structure)
	const savingsPlan = {
		name: planName,
		contribution: monthlyContribution,
		dueDate: dueDate,
		duration: duration,
	};

	// You can handle the new savings plan data as needed (e.g., save it to a database)

	// Optionally, reset the form after submission
	document.getElementById('planName').value = '';
	document.getElementById('monthlyContribution').value = '';
	document.getElementById('dueDate').value = '';
	document.getElementById('duration').value = '';

	alert('Savings plan created successfully!');
}

// Add a submit event listener to the form
const savingsForm = document.querySelector('.savings-form form');
if (savingsForm) {
	savingsForm.addEventListener('submit', function (e) {
		e.preventDefault(); // Prevent the default form submission
		createSavingsPlan();
	});
}
