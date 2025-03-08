// Initialize variables for blur intensity and scaling
let blurIntensity = 0;
let scale = 1;

// Function to apply the blur and scale effects
function blurAndShrink() {
    // Increase blur intensity and reduce scale
    blurIntensity += 0.5;
    scale -= 0.01;

    // Prevent the scale from shrinking to zero
    if (scale < 0.2) scale = 0.2;

    // Apply blur to all elements
    document.body.style.filter = `blur(${blurIntensity}px)`;

    // Apply a shrinking effect to the body
    document.body.style.transform = `scale(${scale})`;
    document.body.style.transformOrigin = "center";

    // Ensure the body's position remains consistent
    document.body.style.overflow = "hidden";
    document.body.style.margin = "0";
    document.body.style.padding = "0";
}

// Set an interval to continuously increase the effect
setInterval(blurAndShrink, 100); // Adjust interval time for slower or faster progression
