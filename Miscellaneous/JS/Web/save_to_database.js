const BASE_URL = "https://your-api.com/api"; // Change this to your actual API URL

// Function for database interactions
async function save_to_database() {
    try {
        // [Single Value Save] - Save individual key-value pair (e.g., User Token)
        const singleData = { key: "user_token", value: "placeholder_token_12345" };
        let response = await fetch(`${BASE_URL}/save-single`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(singleData),
        });
        console.log("Single Value Save:", await response.json());

        // [Multi-Value Save] - Save multiple key-value pairs at once
        const multiData = {
            username: "placeholder_user",
            email: "placeholder@example.com",
            theme: "dark",
            notifications: true,
        };
        response = await fetch(`${BASE_URL}/save-multiple`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(multiData),
        });
        console.log("Multi-Value Save:", await response.json());

        // [Save JSON Object] - Save complex objects as JSON
        const jsonData = {
            profile: {
                name: "Placeholder Name",
                age: 25,
                preferences: {
                    language: "en",
                    colorScheme: "light",
                },
            },
        };
        response = await fetch(`${BASE_URL}/save-json`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(jsonData),
        });
        console.log("JSON Object Save:", await response.json());
    } catch (error) {
        console.error("Error saving data:", error);
    }
}

// Call the function to save placeholder data
save_to_database();

// Fetching requests to GET elements from the database
async function get_from_database() {
    try {
        // [Fetch Single Value] (e.g., User Token)
        let response = await fetch(`${BASE_URL}/get-single?key=user_token`);
        let singleData = await response.json();
        console.log("Retrieved Single Value:", singleData);

        // [Fetch Multi-Value Data]
        response = await fetch(`${BASE_URL}/get-multiple`);
        let multiData = await response.json();
        console.log("Retrieved Multi-Value Data:", multiData);

        // [Fetch JSON Object]
        response = await fetch(`${BASE_URL}/get-json`);
        let jsonData = await response.json();
        console.log("Retrieved JSON Data:", jsonData);
    } catch (error) {
        console.error("Error fetching data:", error);
    }
}

// Call the function to retrieve data
get_from_database();

// Function for database updates. If used update params!
async function update_database() {
    try {
        const updatedData = {
            key: "user_profile",
            newValue: {
                profile: {
                    name: "Updated Name",
                    age: 30,
                    preferences: {
                        language: "fr",
                        colorScheme: "dark",
                    },
                },
            },
        };

        let response = await fetch(`${BASE_URL}/update`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(updatedData),
        });

        console.log("Update Response:", await response.json());
    } catch (error) {
        console.error("Error updating data:", error);
    }
}

// Call the function to update data
update_database();

// Function to delete elements from the database
async function delete_from_database() {
    try {
        const keyToDelete = { key: "user_token" };

        let response = await fetch(`${BASE_URL}/delete`, {
            method: "DELETE",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(keyToDelete),
        });

        console.log("Delete Response:", await response.json());
    } catch (error) {
        console.error("Error deleting data:", error);
    }
}

// Call the function to delete data
delete_from_database();
