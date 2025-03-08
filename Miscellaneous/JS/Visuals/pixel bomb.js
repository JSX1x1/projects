// Initialize variables for pixelation intensity and glitch effects
let pixelation = 1;
let glitchInterval = 50; // Faster glitch updates
let noiseIntensity = 10; // Intensity of the glitch noise effect

// Create a canvas to apply the pixelation effect
const canvas = document.createElement("canvas");
const ctx = canvas.getContext("2d");
document.body.appendChild(canvas);

// Set canvas to cover the entire viewport
canvas.style.position = "fixed";
canvas.style.top = "0";
canvas.style.left = "0";
canvas.style.width = "100%";
canvas.style.height = "100%";
canvas.style.zIndex = "9999";
canvas.style.pointerEvents = "none"; // Allow interaction with the page
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

// Function to capture the page and pixelate it progressively, stacking the effect
function pixelatePage() {
    // Capture the current page as an image
    html2canvas(document.body).then((screenshot) => {
        const image = new Image();
        image.src = screenshot.toDataURL();
        image.onload = () => {
            // Clear the canvas
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Aggressive pixelation with reduced resolution
            const reducedWidth = Math.max(5, canvas.width / pixelation); // Faster and larger pixelation
            const reducedHeight = Math.max(5, canvas.height / pixelation); // Faster and larger pixelation

            // Draw the image with reduced resolution (pixelation effect)
            ctx.drawImage(image, 0, 0, reducedWidth, reducedHeight);
            ctx.drawImage(canvas, 0, 0, reducedWidth, reducedHeight, 0, 0, canvas.width, canvas.height);

            // Gradually increase pixelation intensity
            pixelation += 1.5; // Faster increase in pixelation
        };
    });
}

// Function to add random glitch noise to the page, making it worse
function addGlitchNoise() {
    const noiseCanvas = document.createElement("canvas");
    const noiseCtx = noiseCanvas.getContext("2d");
    noiseCanvas.width = window.innerWidth;
    noiseCanvas.height = window.innerHeight;

    // Create a random noise pattern
    const imageData = noiseCtx.createImageData(noiseCanvas.width, noiseCanvas.height);
    const data = imageData.data;

    for (let i = 0; i < data.length; i += 4) {
        // Random noise for each pixel
        data[i] = Math.random() * 255; // Red channel
        data[i + 1] = Math.random() * 255; // Green channel
        data[i + 2] = Math.random() * 255; // Blue channel
        data[i + 3] = Math.random() * 255; // Alpha channel (transparency)
    }

    noiseCtx.putImageData(imageData, 0, 0);

    // Overlay the noise on top of the canvas
    const noiseImage = new Image();
    noiseImage.src = noiseCanvas.toDataURL();
    noiseImage.onload = () => {
        ctx.drawImage(noiseImage, 0, 0, canvas.width, canvas.height);
    };
}

// Function to spawn glitchy rainbow squares that persist and clutter the screen
function spawnGlitchSquare() {
    const square = document.createElement("div");
    square.style.position = "absolute";
    square.style.width = `${Math.random() * 150 + 50}px`;
    square.style.height = `${Math.random() * 150 + 50}px`;
    square.style.top = `${Math.random() * window.innerHeight}px`;
    square.style.left = `${Math.random() * window.innerWidth}px`;
    square.style.backgroundColor = `rgba(${Math.random() * 255}, ${Math.random() * 255}, ${Math.random() * 255}, 0.8)`;
    square.style.pointerEvents = "none"; // Ensure it doesn't interfere with the page

    document.body.appendChild(square);
}

// Continuously pixelate the page, with faster updates for more severe effect
setInterval(pixelatePage, 10); // Much faster pixelation updates for more aggressive effect

// Add glitch noise at an intense rate
setInterval(addGlitchNoise, glitchInterval); // Random noise overlay every 50ms

// Spawn glitchy rainbow squares at random intervals, aggressively increasing chaos
setInterval(spawnGlitchSquare, 50); // Extremely frequent square spawning for maximum chaos
