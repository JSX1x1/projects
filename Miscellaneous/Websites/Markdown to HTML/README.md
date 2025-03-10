# Markdown to HTML Parser

This project allows you to upload a Markdown file (.md) and converts it to HTML for easy viewing. The page uses a retro, old-school tech style and includes a simple interface where the user can select a Markdown file, and the content will be parsed and displayed in a readable HTML format.

## Features

- Upload `.md` or `.markdown` files directly from your local system.
- Convert Markdown into clean, readable HTML.
- Display the parsed HTML with an old-school tech style (monospace fonts, neon colors, etc.).
- Simple and user-friendly interface for easy file selection and parsing.

## Requirements

- A modern web browser (Chrome, Firefox, Safari, etc.) to view and interact with the HTML page.

## File Structure

```
/your-project-directory
    ├── index.html      # Main HTML file for structure and layout
    ├── style.css       # CSS file for styling the page (retro tech theme)
    └── script.js       # JavaScript file for handling file upload and Markdown parsing
```

## How to Use

1. **Clone the Repository** (if applicable):

   If you're cloning the repository, run the following command:

   ```bash
   git clone https://github.com/your-username/markdown-to-html-parser.git
   ```

2. **Open the `index.html` file**:

   - Simply open the `index.html` file in your web browser (by double-clicking it or using your browser's `Open File` option).
   
3. **Upload a Markdown File**:
   - Click the **"Choose File"** button on the webpage.
   - Select any `.md` or `.markdown` file from your computer.

4. **View the Parsed HTML**:
   - After uploading, the Markdown content will be parsed into HTML and displayed directly on the page in a readable format.

5. **Tech Style Display**:
   - The page uses an old-school tech theme with a monospace font and neon colors for that nostalgic feel.

## Technologies Used

- **HTML5** for the structure and layout of the page.
- **CSS3** for styling and creating the retro tech look.
- **JavaScript** (using the `marked.js` library) for parsing the Markdown content into HTML.
- **marked.js**: A JavaScript library for converting Markdown into HTML.

## Customization

If you'd like to customize the look of the page, you can adjust the styles in `style.css`. You can change things like:

- Font family
- Background and text colors
- Layout and margins
- Hover effects for buttons

Additionally, you can modify the JavaScript file (`script.js`) if you wish to extend functionality (e.g., supporting other file types, adding more advanced features, etc.).

## Troubleshooting

- **File not converting?** Make sure you are selecting a valid `.md` or `.markdown` file. The file must be a plain text Markdown file.
- **Page not rendering correctly?** Try opening the page in a different browser or clearing your browser cache.

---

## Acknowledgments

- Thanks to the developers of the `marked.js` library for providing an easy-to-use solution for Markdown parsing.
- This project is inspired by early web development and retro computer interfaces, designed to look like an old-school terminal.