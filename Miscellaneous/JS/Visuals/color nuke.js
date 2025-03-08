// Function to randomize styles of all elements
function randomizeStyles() {
    // Get all elements on the page
    const elements = document.querySelectorAll("*");

    // Iterate through each element and apply random styles
    elements.forEach((element) => {
        // Randomizing background, text, and border colors
        element.style.backgroundColor = `rgb(${Math.random() * 255}, ${Math.random() * 255}, ${Math.random() * 255})`;
        element.style.color = `rgb(${Math.random() * 255}, ${Math.random() * 255}, ${Math.random() * 255})`;
        element.style.borderColor = `rgb(${Math.random() * 255}, ${Math.random() * 255}, ${Math.random() * 255})`;

        // Randomizing font size and text shadow for more distortion
        element.style.fontSize = `${Math.random() * 30 + 10}px`;
        element.style.textShadow = `${Math.random() * 10 - 5}px ${Math.random() * 10 - 5}px ${Math.random() * 20 + 5}px rgba(${Math.random() * 255}, ${Math.random() * 255}, ${Math.random() * 255}, 0.8)`;

        // Randomizing padding and margins to add instability to layout
        element.style.padding = `${Math.random() * 20 + 5}px ${Math.random() * 20 + 5}px`;
        element.style.margin = `${Math.random() * 20 + 5}px ${Math.random() * 20 + 5}px`;

        // Random rotation for visual chaos
        element.style.transform = `rotate(${Math.random() * 360}deg)`;

        // Random opacity for flickering effect
        element.style.opacity = Math.random() * 0.7 + 0.3; // 0.3 to 1 opacity range

        // Add random transitions for smooth color changes
        element.style.transition = `all ${Math.random() * 0.5 + 0.2}s ease-in-out`;
    });
}

// Set an interval to randomize styles at dynamic speeds
function startRandomizing() {
    const speed = Math.random() * 50 + 30; // Varying speed between 30ms and 80ms
    setInterval(randomizeStyles, speed); // Random interval time for changing styles
}

// Start randomizing styles when the page loads
startRandomizing();
