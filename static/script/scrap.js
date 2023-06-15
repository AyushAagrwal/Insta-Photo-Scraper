document
  .getElementById("scrapForm")
  .addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent form submission

    // Make an AJAX request to call the '/scrap_photos' endpoint
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/scrap_photos");
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onload = function () {
      if (xhr.status === 200) {
        var message = document.createElement("h1");
        message.innerHTML = "Scraping photos successful";
        document.body.appendChild(message);
      } else {
        var message = document.createElement("h1");
        message.innerHTML = "Scraping photos failed";
        document.body.appendChild(message);
      }
    };

    xhr.send();
  });
