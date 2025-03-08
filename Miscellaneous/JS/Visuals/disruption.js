// Overwrite the entire HTML content
document.body.innerHTML = "";

// Set body styles for complete disruption
document.body.style.backgroundColor = "black";
document.body.style.color = "red";
document.body.style.fontFamily = "monospace";
document.body.style.textAlign = "center";
document.body.style.paddingTop = "20%";
document.body.style.fontSize = "20px";
document.body.style.overflow = "hidden";

// Create the binary disruption text
const binaryText = document.createElement("div");
binaryText.textContent =
    "01010000 01100001 01100111 01100101 00100000 01101000 01100001 01110011 00100000 01100010 01100101 01100101 01101110 00100000 01100100 01101001 01110011 01110010 01110101 01110000 01110100 01100101 01100100 00100000 01100010 01111001 00100000 01000010 00110001 00110100 01000011 01001011 00110000 01010101 01010100";

// Append the binary text to the body
document.body.appendChild(binaryText);
