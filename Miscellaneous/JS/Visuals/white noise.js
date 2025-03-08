// Function to generate and apply white noise to all elements
function applyWhiteNoiseToElements() {
    // Create a function to generate white noise as a data URL
    function generateWhiteNoise() {
        const canvas = document.createElement("canvas");
        const ctx = canvas.getContext("2d");
        const width = 100;
        const height = 100;
        canvas.width = width;
        canvas.height = height;

        const imageData = ctx.createImageData(width, height);
        const data = imageData.data;

        for (let i = 0; i < data.length; i += 4) {
            const gray = Math.random() * 255; // Random grayscale value
            data[i] = gray;       // Red
            data[i + 1] = gray;   // Green
            data[i + 2] = gray;   // Blue
            data[i + 3] = 255;    // Alpha
        }

        ctx.putImageData(imageData, 0, 0);
        return canvas.toDataURL();
    }

    // Generate the initial white noise data URL
    const noiseImage = generateWhiteNoise();

    // Apply the white noise background to all elements
    const allElements = document.querySelectorAll("*");
    allElements.forEach(element => {
        element.style.backgroundImage = `url(${noiseImage})`;
        element.style.backgroundSize = "cover";
        element.style.animation = "whiteNoiseEffect 0.1s infinite linear";
    });

    // Add keyframes for the white noise effect
    const styleSheet = document.styleSheets[0] || document.createElement("style");
    if (!document.styleSheets[0]) document.head.appendChild(styleSheet);
    styleSheet.insertRule(`
        @keyframes whiteNoiseEffect {
            0% { background-image: url(${generateWhiteNoise()}); }
            100% { background-image: url(${generateWhiteNoise()}); }
        }
    `, styleSheet.cssRules.length);
}

// Activate the white noise effect
applyWhiteNoiseToElements();
