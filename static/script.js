fetch('header.html')
    .then(response => response.text())
    .then(html => document.getElementById('header').innerHTML = html);
fetch('footer.html')
    .then(response => response.text())
    .then(html => document.getElementById('footer').innerHTML = html);

// // login scripting


// document.addEventListener('DOMContentLoaded', function() {
//     const form = document.querySelector('form');

//     form.addEventListener('submit', function(event) {
//         event.preventDefault();


//         const email = document.querySelector('input[name="email"]').value;
//         const password = document.querySelector('input[name="password"]').value;


//         if (!email.trim()) {
//             alert('Please enter your email.');
//             return;
//         }

//         if (!password.trim()) {
//             alert('Please enter your password.');
//             return;
//         }


//         form.submit();
//     });
// });


// // Signup validation

// document.addEventListener('DOMContentLoaded', function() {
//     const form = document.querySelector('form');

//     form.addEventListener('submit', function(event) {
//         const usernameInput = document.querySelector('input[name="username"]');
//         const username = usernameInput.value;

//         // Validate the username for special characters
//         const usernameRegex = /^[a-zA-Z0-9]+$/; // Regular expression to allow only alphanumeric characters
//         if (!usernameRegex.test(username)) {
//             event.preventDefault(); // Prevent the form from submitting
//             alert('Username can only contain letters and numbers.'); // Display an error message
//             return;
//         }

//         const passwordInput = document.querySelector('input[name="password"]');
//         const password = passwordInput.value;

//         // Validate the password for length and special characters
//         if (password.length < 8) {
//             event.preventDefault(); // Prevent the form from submitting
//             alert('Password must be at least 8 characters long.'); // Display an error message
//             return;
//         }

//         const passwordRegex = /^[a-zA-Z0-9!@#$%^&*()_+{}\[\]:;<>,.?~\-]+$/; // Regular expression to allow alphanumeric characters and some special symbols
//         if (!passwordRegex.test(password)) {
//             event.preventDefault(); // Prevent the form from submitting
//             alert('Password can only contain letters, numbers, and the following symbols: !@#$%^&*()_+{}[]:;<>,.?~-'); // Display an error message
//             return;
//         }
//     });
// });