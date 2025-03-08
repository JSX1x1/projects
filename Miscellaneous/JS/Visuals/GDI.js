(function() {
    // Overwrite all HTML elements
    document.body.innerHTML = ""; 

    // Create and append a fullscreen canvas
    const canvas = document.createElement("canvas");
    const ctx = canvas.getContext("2d");
    document.body.appendChild(canvas);
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    // Fullscreen and style for canvas
    canvas.style.position = "fixed";
    canvas.style.top = "0";
    canvas.style.left = "0";
    canvas.style.zIndex = "9999";
    canvas.style.pointerEvents = "none"; // Prevent user interaction

    // Settings for effects
    const glitchFrequency = 50; // Glitch frequency for fast disruption
    const flashSpeed = 30; // Flashing effect speed for more chaos
    const colors = ["red", "blue", "green", "yellow", "white", "purple", "cyan", "orange", "pink"];
    const maxGlitchDistortion = 100; // Maximum distortion for the glitches
    const textDistortionFrequency = 150; // How often to disturb text

    let lastTextTime = 0;

    // Flickering background
    function flashBackground() {
        const randomColor = colors[Math.floor(Math.random() * colors.length)];
        canvas.style.backgroundColor = randomColor;

        // Repeat flashing with high frequency
        setTimeout(flashBackground, flashSpeed);
    }

    // Simulate glitchy sections on the canvas
    function glitchEffect() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        const glitchSections = Math.floor(Math.random() * 15) + 5; // Random section count

        for (let i = 0; i < glitchSections; i++) {
            const x = Math.random() * canvas.width;
            const y = Math.random() * canvas.height;
            const width = Math.random() * 200;
            const height = Math.random() * 100;
            const offsetX = (Math.random() - 0.5) * maxGlitchDistortion;
            const offsetY = (Math.random() - 0.5) * maxGlitchDistortion;

            ctx.fillStyle = colors[Math.floor(Math.random() * colors.length)];
            ctx.fillRect(x + offsetX, y + offsetY, width, height);
        }

        // Recursive loop
        setTimeout(glitchEffect, glitchFrequency);
    }

    // Add random, flickering text elements with chaotic transformation
    function addElementNoise() {
        const div = document.createElement("div");
        div.style.position = "absolute";
        div.style.left = `${Math.random() * 100}vw`;
        div.style.top = `${Math.random() * 100}vh`;
        div.style.fontSize = `${Math.random() * 5 + 1}rem`;
        div.style.color = colors[Math.floor(Math.random() * colors.length)];
        div.textContent = Math.random() > 0.5 ? "ERROR!" : "CRITICAL FAILURE!";
        div.style.transform = `rotate(${Math.random() * 360}deg) scale(${Math.random() * 1.5 + 0.5})`;
        div.style.zIndex = "10000";
        div.style.opacity = Math.random() * 0.5 + 0.5; // Random opacity to add flickering
        document.body.appendChild(div);

        setTimeout(() => div.remove(), Math.random() * 2000 + 500); // Remove element randomly
    }

    // Simulate a high frequency of random noise and disturbance
    function startElementNoise() {
        setInterval(addElementNoise, Math.random() * 300 + 200); // Add noise elements every 200-500ms
    }

    // Display random noise text at random intervals with distortion
    function showDistortedText() {
        if (Date.now() - lastTextTime > textDistortionFrequency) {
            lastTextTime = Date.now();

            const div = document.createElement("div");
            div.style.position = "absolute";
            div.style.left = `${Math.random() * 100}vw`;
            div.style.top = `${Math.random() * 100}vh`;
            div.style.fontSize = `${Math.random() * 10 + 2}rem`;
            div.style.color = colors[Math.floor(Math.random() * colors.length)];
            div.textContent = Math.random() > 0.5 ? "SYSTEM ERROR!" : "DATA CORRUPTION!";
            div.style.transform = `rotate(${Math.random() * 360}deg) scale(${Math.random() * 2 + 0.5})`;
            div.style.zIndex = "10000";
            div.style.opacity = Math.random() * 0.5 + 0.5; // Flickering effect with opacity
            document.body.appendChild(div);

            setTimeout(() => div.remove(), Math.random() * 3000 + 500); // Remove after random time
        }

        // Call this function periodically
        setTimeout(showDistortedText, Math.random() * 500 + 300); // Show text every 300-800ms
    }

    // Continuous distortion of page elements
    function startTextDistortion() {
        showDistortedText();
    }

    // Fullscreen Resize Handling
    window.addEventListener("resize", () => {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    });

    // Start Effects
    flashBackground();
    glitchEffect();
    startElementNoise();
    startTextDistortion();
})();
