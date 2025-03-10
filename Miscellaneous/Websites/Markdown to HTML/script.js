// Grab the file input element and output area
const fileInput = document.getElementById('markdown-file');
const outputArea = document.getElementById('output');

// Function to read the selected file and convert markdown to HTML
fileInput.addEventListener('change', (event) => {
    const file = event.target.files[0];
    
    if (file && file.type === 'text/markdown' || file.name.endsWith('.md')) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            const markdownText = e.target.result;
            // Use the 'marked' library to parse the markdown
            const htmlContent = marked(markdownText);
            // Output the parsed HTML into the output area
            outputArea.innerHTML = htmlContent;
        };
        
        reader.onerror = function() {
            alert("There was an error reading the file.");
        };
        
        reader.readAsText(file);
    } else {
        alert("Please select a valid Markdown (.md) file.");
    }
});
