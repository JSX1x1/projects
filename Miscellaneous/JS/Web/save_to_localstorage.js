// This function provides multiple sections of different save typed that can be used and modified dynamically

function save_to_localstorage() {
    // [Single Value Safe] - Save individual key-value pair
    // Remove this section if not needed
    const singleKey = "user_token";                // Example key
    const singleValue = "placeholder_token_12345";  // Example value
    localStorage.setItem(singleKey, JSON.stringify(singleValue));
    console.log(`Saved ${singleKey}: ${singleValue} to LocalStorage.`);

    // [Multi Value Safe] - Save multiple key-value pairs at once
    // Remove this section if not needed
    const multiData = {
        username: "placeholder_user",        // Example: Replace with dynamic username
        email: "placeholder@example.com",    // Example: Replace with dynamic email
        theme: "dark",                       // Example: Replace with user-selected theme
        notifications: true,                 // Example: Replace with user's preference
    };

    for (const [key, value] of Object.entries(multiData)) {
        localStorage.setItem(key, JSON.stringify(value));
        console.log(`Saved ${key}: ${value} to LocalStorage.`);
    }

    // [Save JSON Object] - Save complex objects as JSON strings
    // Remove this section if not needed
    const jsonData = {
        profile: {
            name: "Placeholder Name",
            age: 25,
            preferences: {
                language: "en",
                colorScheme: "light"
            }
        }
    };
    localStorage.setItem("user_profile", JSON.stringify(jsonData));
    console.log(`Saved user_profile to LocalStorage.`);
}

// Call the function to save placeholder data
save_to_localstorage();


// This function is used to clear the localstorage completly from all elements.
// If certain elements are wanted to be removed the code needs to be adjusted to the right params.

function clear_localstorage() {
    localStorage.clear(); // Clears all data
    console.log("LocalStorage has been cleared.");
}

// Call when necessary
clear_localstorage();
