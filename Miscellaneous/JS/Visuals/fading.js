// Function to create the fading effect and add white dots afterward
function applyFadingAndDots() {
    // Create a div to overlay the page and cover it with black
    const fadeOverlay = document.createElement("div");
    fadeOverlay.style.position = "fixed";
    fadeOverlay.style.top = "0";
    fadeOverlay.style.left = "0";
    fadeOverlay.style.width = "100%";
    fadeOverlay.style.height = "100%";
    fadeOverlay.style.backgroundColor = "black";
    fadeOverlay.style.zIndex = "9999"; // Ensure it covers all elements
    fadeOverlay.style.pointerEvents = "none"; // Make sure it doesn't interfere with interaction
    document.body.appendChild(fadeOverlay);

    // Apply the fading effect
    let opacity = 0;
    const fadeInterval = setInterval(() => {
        opacity += 0.02; // Increase opacity gradually
        fadeOverlay.style.opacity = opacity;

        // Once the page is fully black, stop the interval and start the dots
        if (opacity >= 1) {
            clearInterval(fadeInterval);
            startRandomDots(); // Start the white dots after fading
        }
    }, 50); // Adjust the speed of the fade here
}

// Function to start random white dots covering the screen
function startRandomDots() {
    // Create random white dots that will slowly cover the screen
    setInterval(() => {
        const dot = document.createElement("div");
        dot.style.position = "absolute";
        dot.style.width = `${Math.random() * 20 + 5}px`;  // Random dot size
        dot.style.height = `${Math.random() * 20 + 5}px`; // Random dot size
        dot.style.backgroundColor = "white";
        dot.style.borderRadius = "50%"; // Make it a perfect circle
        dot.style.top = `${Math.random() * window.innerHeight}px`;  // Random position
        dot.style.left = `${Math.random() * window.innerWidth}px`; // Random position
        dot.style.opacity = "0.8";  // Slight transparency for effect
        dot.style.pointerEvents = "none"; // Allow interaction with underlying page elements

        // Append dot to the body
        document.body.appendChild(dot);

        // Gradually increase the opacity and size of the dot for more effect
        setTimeout(() => {
            dot.style.width = `${parseInt(dot.style.width) * 2}px`;  // Increase dot size
            dot.style.height = `${parseInt(dot.style.height) * 2}px`; // Increase dot size
            dot.style.opacity = "1"; // Make it fully opaque
        }, 100);

    }, 100); // Create new dots every 100ms
}

// Apply the fading effect and dots after the fade
applyFadingAndDots();
