// Initialize dark mode setting from local storage
const themeToggleButton = document.getElementById("theme-toggle-btn");
const body = document.body;
const outputDiv = document.getElementById("output");
const fileInput = document.getElementById("xml-file");

let isDarkMode = localStorage.getItem("darkMode") === "true";
if (isDarkMode) {
    body.classList.add("dark-mode");
    themeToggleButton.textContent = "Switch to Light Mode";
} else {
    body.classList.add("light-mode");
    themeToggleButton.textContent = "Switch to Dark Mode";
}

// Theme toggle functionality
themeToggleButton.addEventListener("click", () => {
    isDarkMode = !isDarkMode;

    if (isDarkMode) {
        body.classList.remove("light-mode");
        body.classList.add("dark-mode");
        themeToggleButton.textContent = "Switch to Light Mode";
    } else {
        body.classList.remove("dark-mode");
        body.classList.add("light-mode");
        themeToggleButton.textContent = "Switch to Dark Mode";
    }

    // Save the theme preference in local storage
    localStorage.setItem("darkMode", isDarkMode);
});

// Function to parse XML to readable HTML
function parseXMLToHTML(xmlString) {
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(xmlString, "application/xml");
    const elements = xmlDoc.documentElement.childNodes;

    let htmlContent = "<h2>XML Structure:</h2><ul>";

    function processNode(node) {
        if (node.nodeType === 1) {
            htmlContent += `<li><strong>${node.nodeName}:</strong>`;
            if (node.hasChildNodes()) {
                htmlContent += "<ul>";
                node.childNodes.forEach(childNode => processNode(childNode));
                htmlContent += "</ul>";
            } else {
                htmlContent += ` ${node.textContent}</li>`;
            }
        }
    }

    elements.forEach(element => processNode(element));
    htmlContent += "</ul>";

    return htmlContent;
}

// Event listener for XML file input
fileInput.addEventListener("change", (e) => {
    const file = e.target.files[0];
    if (file && file.type === "application/xml") {
        const reader = new FileReader();
        reader.onload = function (event) {
            const xmlString = event.target.result;
            const htmlContent = parseXMLToHTML(xmlString);
            outputDiv.innerHTML = htmlContent;
        };
        reader.readAsText(file);
    } else {
        outputDiv.innerHTML = "Please select a valid XML file.";
    }
});
