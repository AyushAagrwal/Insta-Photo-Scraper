// Add an active class to the current navbar link
var navbarItems = document.querySelectorAll(".navbar li a");

navbarItems.forEach(function (item) {
  item.addEventListener("click", function () {
    navbarItems.forEach(function (navbarItem) {
      navbarItem.classList.remove("active");
    });
    this.classList.add("active");
  });
});

// Prevent form submission and perform custom actions
document
  .getElementById("loginForm")
  .addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent form submission

    // Perform any custom actions here
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;

    // Example: Display a message with the entered username and password
    alert("Username: " + username + "\nPassword: " + password);

    // You can also use AJAX to send the form data to the server for authentication
  });
