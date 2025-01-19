// scripts.js

// Confirmation dialog for delete actions
function confirmDelete(event) {
    const confirmMessage = "Are you sure you want to delete this item? This action cannot be undone.";
    if (!confirm(confirmMessage)) {
        event.preventDefault(); // Prevents the default action if user cancels
    }
}

// Attach the confirmDelete function to all delete buttons or links
document.addEventListener("DOMContentLoaded", function () {
    const deleteButtons = document.querySelectorAll(".btn-danger");
    deleteButtons.forEach(button => {
        button.addEventListener("click", confirmDelete);
    });
});

// Basic form validation
function validateForm(event) {
    const form = event.target;
    let valid = true;
    const inputs = form.querySelectorAll("input, textarea, select");

    inputs.forEach(input => {
        if (input.hasAttribute("required") && !input.value.trim()) {
            valid = false;
            alert(`The field "${input.name}" is required.`);
            input.focus();
        }
    });

    if (!valid) {
        event.preventDefault(); // Prevents form submission if validation fails
    }
}

// Attach validateForm to all forms
document.addEventListener("DOMContentLoaded", function () {
    const forms = document.querySelectorAll("form");
    forms.forEach(form => {
        form.addEventListener("submit", validateForm);
    });
});

// Dynamic interaction for form inputs (e.g., movie rating slider)
document.addEventListener("DOMContentLoaded", function () {
    const ratingInput = document.querySelector("#movieRating");
    const ratingDisplay = document.querySelector("#ratingValue");

    if (ratingInput && ratingDisplay) {
        ratingInput.addEventListener("input", function () {
            ratingDisplay.textContent = ratingInput.value;
        });
    }
});
