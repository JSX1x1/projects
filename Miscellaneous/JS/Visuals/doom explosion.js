// Function to create the enhanced Doom Explosion effect
function doomExplosion() {
    // Create the explosion effect container
    const explosion = document.createElement("div");
    explosion.style.position = "fixed";
    explosion.style.top = "0";
    explosion.style.left = "0";
    explosion.style.width = "100vw";
    explosion.style.height = "100vh";
    explosion.style.background = "radial-gradient(circle, rgba(255, 0, 0, 1), rgba(255, 165, 0, 0.6), rgba(255, 255, 255, 0.3))";
    explosion.style.zIndex = "9999";
    explosion.style.pointerEvents = "none"; // Allow interaction with elements underneath
    explosion.style.opacity = "1";
    explosion.style.animation = "explosion 1.5s ease-in-out forwards, shockwave 0.5s linear forwards";
    explosion.style.transformOrigin = "center"; // Make the explosion grow from the center
    
    // Append explosion element to body
    document.body.appendChild(explosion);

    // Add the keyframes for explosion and shockwave animations to the page
    const styleSheet = document.createElement("style");
    styleSheet.innerHTML = `
        @keyframes explosion {
            0% { transform: scale(0); opacity: 1; }
            100% { transform: scale(40); opacity: 0; }
        }
        @keyframes shockwave {
            0% { transform: scale(1); opacity: 1; }
            100% { transform: scale(50); opacity: 0.2; }
        }
    `;
    document.head.appendChild(styleSheet);

    // Variables for shaking effect
    let shakeIntensity = 10; // Initial shake intensity
    let shakeInterval = 15; // Initial shake interval (ms)

    // Function to shake the page violently and erratically
    function shakePage() {
        // Increase shake intensity over time for more violent shaking
        shakeIntensity += Math.random() * 3; // Add randomness to shake intensity
        shakeInterval = Math.max(5, shakeInterval - 1); // Decrease interval to make the shake faster

        // Apply random shaking movement
        document.body.style.transform = `translate(${Math.random() * shakeIntensity - shakeIntensity / 2}px, ${Math.random() * shakeIntensity - shakeIntensity / 2}px) rotate(${Math.random() * 10 - 5}deg)`;

        // Continue shaking at an increasing speed
        setTimeout(shakePage, shakeInterval);
    }

    // Start shaking effect
    shakePage();

    // Add explosion sound effect (optional)
    const audio = new Audio('https://www.soundjay.com/button/beep-07.wav'); // Replace with explosion sound URL
    audio.play();

    // After the explosion animation ends, remove the explosion element
    setTimeout(() => {
        explosion.remove();
    }, 1500); // Match the explosion duration
}

// Activate the enhanced Doom Explosion effect
doomExplosion();

