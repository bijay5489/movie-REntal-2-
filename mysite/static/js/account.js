function createAccount() {
    var firstName = $("#first-name").val().trim();
    var lastName = $("#last-name").val().trim();
    var email = $("#email").val().trim();

    // Post data to the server
    $.post("/dbUser/", { "first_name": firstName, "last_name": lastName, "email": email })
        .done(function(data) {
            // Handle success
            $("#success-message").text("Account created successfully for " + data.first_name + " " + data.last_name);
            $("#error-message").text("");
        })
        .fail(function(xhr) {
            // Handle failure
            var response = xhr.responseJSON;
            var errorMessage = "Failed to create account.";

            // Make sure response exists and has a property 'errors' or 'error'
            if (response && response.errors) {
                errorMessage = parseFormErrors(response.errors);
            } else if (response && response.error) {
                errorMessage = response.error;
            } else {
                errorMessage = "An unknown error occurred.";
            }

            $("#error-message").text(errorMessage);
            $("#success-message").text(""); // Clear any previous success message
        });
}

function parseFormErrors(errors) {
    var message = [];
    for (var key in errors) {
        if (errors.hasOwnProperty(key)) {
            // Concatenate the key and its errors into a string
            message.push(key + ": " + errors[key].map(function(error) { return error.message; }).join(", "));
        }
    }
    return message.join(" | ");
}
