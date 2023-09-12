// Get references to the buttons
const studentButton = document.getElementById('studentButton');
const employedButton = document.getElementById('employedButton');
const selfEmployedButton = document.getElementById('selfEmployedButton');

// Function to toggle button color on click
function toggleButtonColor(button) {
	button.classList.toggle('btn-clicked');
}

// Add click event listeners to the buttons
studentButton.addEventListener('click', () => toggleButtonColor(studentButton));
employedButton.addEventListener('click', () => toggleButtonColor(employedButton));
selfEmployedButton.addEventListener('click', () => toggleButtonColor(selfEmployedButton));
