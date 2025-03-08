// Function to create a random circle snake on the page
function spawnCircleSnake() {
    // Create a container for the snake
    const snakeContainer = document.createElement("div");
    snakeContainer.style.position = "absolute";
    snakeContainer.style.top = `${Math.random() * window.innerHeight}px`;
    snakeContainer.style.left = `${Math.random() * window.innerWidth}px`;
    snakeContainer.style.pointerEvents = "none"; // Ensure it doesn't interfere with page elements

    document.body.appendChild(snakeContainer);

    const segments = [];
    const maxSegments = 50; // Maximum number of circle segments per snake
    let direction = Math.random() * Math.PI * 2;

    // Function to update and draw the snake
    function updateSnake() {
        // Create a new circle segment
        const circle = document.createElement("div");
        circle.style.width = "10px";
        circle.style.height = "10px";
        circle.style.borderRadius = "50%";
        circle.style.backgroundColor = `rgba(${Math.random() * 255}, ${Math.random() * 255}, ${Math.random() * 255}, 0.8)`;
        circle.style.position = "absolute";
        circle.style.top = "0px";
        circle.style.left = "0px";
        snakeContainer.appendChild(circle);

        // Add the new segment to the list
        segments.push(circle);

        // Limit the number of segments
        if (segments.length > maxSegments) {
            const oldSegment = segments.shift();
            snakeContainer.removeChild(oldSegment);
        }

        // Move the snake container in a random direction
        const speed = 3;
        const xOffset = Math.cos(direction) * speed;
        const yOffset = Math.sin(direction) * speed;

        let newTop = parseFloat(snakeContainer.style.top) + yOffset;
        let newLeft = parseFloat(snakeContainer.style.left) + xOffset;

        // Wrap around the screen edges
        if (newTop < 0) newTop = window.innerHeight;
        if (newTop > window.innerHeight) newTop = 0;
        if (newLeft < 0) newLeft = window.innerWidth;
        if (newLeft > window.innerWidth) newLeft = 0;

        snakeContainer.style.top = `${newTop}px`;
        snakeContainer.style.left = `${newLeft}px`;

        // Randomly change direction slightly
        direction += (Math.random() - 0.5) * 0.2;

        // Repeat the update
        requestAnimationFrame(updateSnake);
    }

    // Start the snake animation
    updateSnake();
}

// Spawn a new snake every second
setInterval(spawnCircleSnake, 100);
