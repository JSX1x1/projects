// Function to create the Spinner effect
function spinner() {
    let angle = 0; // Initial rotation angle
    let speed = 1; // Initial speed of rotation (increasing over time)
    
    // Apply CSS to allow the page to spin
    document.body.style.transition = "transform 0.1s linear"; // Smooth transition for spin

    // Function to apply rotation
    function rotatePage() {
        // Update the rotation angle by increasing the speed
        angle += speed;
        speed += 0.1; // Increase the speed over time for faster rotation

        // Apply the rotation transformation to the body element
        document.body.style.transform = `rotate(${angle}deg)`;

        // Continuously rotate the page
        setTimeout(rotatePage, 10); // Speed up the rotation every 10ms
    }

    // Start the spinning effect
    rotatePage();
}

// Activate the Spinner effect
spinner();
