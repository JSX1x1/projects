# XML to HTML Converter

## Overview

The **XML to HTML Converter** is a web application that allows users to upload an XML file, which is then parsed and displayed in a readable HTML format. The app also features a **theme toggle** that enables users to switch between **light mode** and **dark mode**. This project uses **HTML**, **CSS**, and **JavaScript** to provide an interactive and responsive user interface.

---

## Features

- **XML File Upload**: Users can upload an XML file, and the content will be parsed and displayed as a readable HTML structure.
- **Light Mode and Dark Mode**: The application includes a theme toggle that allows users to switch between light mode and dark mode.
- **Responsive Design**: The app is designed to be responsive and works well across various screen sizes and devices.
- **Persistent Theme**: The user's theme preference (light or dark) is saved using `localStorage`, so the theme is preserved even after refreshing the page or reopening the application.

---

## Demo

You can try out the application by opening the `index.html` file in any modern web browser.

---

## How to Use

1. Clone the repository or download the project files.
2. Open the `index.html` file in your browser.
3. Upload an XML file using the file input button.
4. The XML content will be parsed and displayed in a readable format.
5. Toggle between **light mode** and **dark mode** using the "Switch to Dark Mode" button.

---

## Installation

To run the project locally:

1. **Clone this repository**:
   ```bash
   git clone https://github.com/your-username/xml-to-html-converter.git
   ```

2. **Navigate to the project directory**:
   ```bash
   cd xml-to-html-converter
   ```

3. **Open the `index.html` file** in your preferred web browser.

You can also serve the project using any web server for local development (e.g., using VS Code's Live Server extension or Python's built-in HTTP server).

---

## Project Structure

The project consists of the following files:

```
xml-to-html-converter/
│
├── index.html           # Main HTML file
├── style.css            # Stylesheet for light and dark modes
├── script.js            # JavaScript to handle XML parsing and theme toggle
└── README.md            # Project documentation
```

### Explanation of Files:

- **`index.html`**: Contains the HTML structure for the page, including the theme toggle button, file input for XML files, and output display area.
- **`style.css`**: Defines the styles for both light and dark themes, as well as the layout and design for the output.
- **`script.js`**: Contains the logic for theme toggling and XML parsing. It also handles the file input, converts the XML to HTML, and updates the displayed content.

---

## Theme Toggle Feature

The theme toggle allows users to switch between **light mode** and **dark mode**.

- By default, the app loads with **light mode**.
- Clicking the "Switch to Dark Mode" button toggles between light and dark modes.
- The user’s theme preference is saved in the browser’s `localStorage`, ensuring that the selected theme is preserved across page reloads.

---

## Technologies Used

- **HTML**: Used to create the structure of the web page.
- **CSS**: Used for styling the page, including the implementation of light and dark modes.
- **JavaScript**: Used for handling user interactions, parsing XML, and toggling themes.
- **DOM Manipulation**: Used to dynamically display the parsed XML content and manage theme switching.

---

## Contributing

Feel free to fork the repository and submit pull requests if you'd like to contribute improvements, bug fixes, or new features. All contributions are welcome!

### Steps to Contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Make your changes and commit them (`git commit -am 'Add feature'`).
4. Push to your branch (`git push origin feature-name`).
5. Open a pull request on GitHub.

---

## License

This project is open source and available under the [MIT License](https://github.com/JSX1x1/projects/blob/main/Miscellaneous/Websites/LICENSE).

---

## Acknowledgements

- [DOMParser](https://developer.mozilla.org/en-US/docs/Web/API/DOMParser) for parsing XML content in JavaScript.
- [localStorage](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage) for saving theme preferences across sessions.

---

## Contact

For any questions or suggestions, feel free to open an issue on the GitHub repository.