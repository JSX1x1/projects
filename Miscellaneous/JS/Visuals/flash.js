// Overwrite the entire HTML content
document.body.innerHTML = "";

// Create a fullscreen canvas
const canvas = document.createElement("canvas");
const ctx = canvas.getContext("2d");
document.body.appendChild(canvas);

// Set canvas dimensions
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;
canvas.style.position = "fixed";
canvas.style.top = "0";
canvas.style.left = "0";
canvas.style.zIndex = "9999";

// Settings
const flashSpeed = 30; // Speed of flashes (ms)
const glitchSpeed = 15; // Speed of glitching 1s and 0s (ms)
const fontSizeRange = [12, 72]; // Font size range for binary digits
const binaryCount = 100; // Number of binary digits flinging at a time
const colors = ["black", "white", "grey"]; // Flashing colors

// Store flying binary digits
const binaryDigits = [];

// Initialize binary digits
function initializeBinaryDigits() {
    for (let i = 0; i < binaryCount; i++) {
        binaryDigits.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            size: Math.random() * (fontSizeRange[1] - fontSizeRange[0]) + fontSizeRange[0],
            speedX: (Math.random() - 0.5) * 10,
            speedY: (Math.random() - 0.5) * 10,
            value: Math.random() > 0.5 ? "1" : "0",
        });
    }
}

// Update binary digit positions
function updateBinaryDigits() {
    binaryDigits.forEach((digit) => {
        digit.x += digit.speedX;
        digit.y += digit.speedY;

        // Wrap around screen edges
        if (digit.x < 0) digit.x = canvas.width;
        if (digit.x > canvas.width) digit.x = 0;
        if (digit.y < 0) digit.y = canvas.height;
        if (digit.y > canvas.height) digit.y = 0;
    });
}

// Draw binary digits
function drawBinaryDigits() {
    ctx.font = "bold 20px monospace";
    binaryDigits.forEach((digit) => {
        ctx.fillStyle = "rgb(0, 255, 0)";
        ctx.font = `${digit.size}px monospace`;
        ctx.fillText(digit.value, digit.x, digit.y);
    });
}

// Flash the screen in black, white, and grey
function flashScreen() {
    const randomColor = colors[Math.floor(Math.random() * colors.length)];
    ctx.fillStyle = randomColor;
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Recursive flash loop
    setTimeout(flashScreen, flashSpeed);
}

// Render glitching binary digits
function renderGlitches() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw binary digits
    drawBinaryDigits();

    // Update binary digit positions
    updateBinaryDigits();

    // Recursive loop
    setTimeout(renderGlitches, glitchSpeed);
}

// Handle canvas resize
window.addEventListener("resize", () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
});

// Start the effects
initializeBinaryDigits();
flashScreen();
renderGlitches();
