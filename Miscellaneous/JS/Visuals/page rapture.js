// Function to apply the "Page Rapture" effect
function pageRapture() {
    // Get all elements on the page
    const elements = document.body.getElementsByTagName("*");

    // Iterate over all elements and move them to random positions
    Array.from(elements).forEach(element => {
        const randomX = Math.random() * window.innerWidth;
        const randomY = Math.random() * window.innerHeight;

        // Apply random positions using CSS
        element.style.position = "absolute"; // Ensure elements can be moved freely
        element.style.left = `${randomX}px`;
        element.style.top = `${randomY}px`;

        // Optional: Add transition for a smooth but chaotic move
        element.style.transition = "all 0.5s ease";
    });
}

// Continuously apply the page rapture effect every 2 seconds
setInterval(pageRapture, 20); 
