# Advanced Redirect and Popup Blocker

## Overview

**Advanced Redirect and Popup Blocker** is a versatile tool designed to enhance your web browsing experience by preventing unwanted redirects, popups, and malicious elements across websites. This solution includes both a **JavaScript-based script** and a **Python GUI-based application**, offering flexible options to suit user needs.

The script ensures global applicability, while the Python GUI provides an intuitive interface for managing blocked URLs and integrating seamlessly with browsers.

---

## Features

### JavaScript Script Features
- **Immediate Redirect Blocking**: Prevents redirection to predefined unwanted URLs instantly upon page load.
- **Popup Blocking**: Aggressively blocks popups, including those triggered by `window.open` and click events.
- **Timer-Based Redirect Protection**: Identifies and neutralizes malicious `setTimeout` and `setInterval` redirection attempts.
- **Dynamic Element Removal**: Automatically detects and removes suspicious iframes, scripts, and popup-related HTML elements.
- **MutationObserver Integration**: Monitors DOM changes to block dynamically added malicious elements in real-time.
- **Customizable Settings**: User-defined configurations, such as blocked URL prefixes, monitoring frequency, and feature toggles.

### Python GUI Features
- **User-Friendly Interface**: A Python-based GUI to manage blocked URLs with ease.
- **Blocked URL Management**: Add, edit, and remove blocked URL prefixes using the GUI.
- **File-Based Persistence**: Save and load blocked URL configurations from a file for easy reuse.
- **Integration with Browser**: Export the blocked URL list for use in a browser extension or other tools.

---

## Installation

### For the JavaScript Script
1. Download the script file (`redirect_popup_blocker.js`) from this repository.
2. Include the script in your desired browser environment:
   - For browser extensions, include it as a content script.
   - For manual use, inject it into your browser console or use tools like Tampermonkey/Greasemonkey.

### For the Python GUI Application
1. Install Python (>= 3.8) if not already installed.
2. Install the required Python packages:
   ```bash
   pip install PyQt6
   ```
3. Download the Python script (`redirect_blocker_gui.py`) from this repository.
4. Run the application:
   ```bash
   python redirect_blocker_gui.py
   ```

---

## Usage

### Configuring the JavaScript Script
The script contains a `config` object to customize its behavior:

```javascript
const config = {
    blockedPrefixes: ["example://unwanted-url-prefix/"], // Add unwanted URL prefixes here.
    checkInterval: 200, // Set the monitoring interval in milliseconds.
    enableRedirectBlocking: true, // Toggle redirect blocking on or off.
    enablePopupBlocking: true, // Toggle popup blocking on or off.
    enableMutationObserver: true, // Enable real-time monitoring of DOM changes.
};
```

### Using the Python GUI
1. Launch the GUI by running the Python script.
2. Use the input field to add new blocked URL prefixes.
3. Select an existing URL from the list and click "Remove Selected URL" to delete it.
4. Save the blocked URL list to a file for future use by clicking "Save Block List."
5. The saved file (`blocked_urls.txt`) can be used by other tools, such as browser extensions, to apply the blocking rules dynamically.

---

## How It Works

1. **JavaScript Script**:
   - The script operates in the browser environment and intercepts various methods (`window.open`, `setTimeout`, etc.) to block unwanted behaviors.
   - It continuously monitors for dynamic changes using `MutationObserver`.

2. **Python GUI**:
   - Provides a centralized management interface for blocked URLs, allowing users to easily add, remove, or export them.
   - Works alongside browser extensions or other blocking tools to enhance the blocking experience.

---

## Contribution Guidelines

We welcome contributions to improve and expand the functionality of this project! Here's how you can help:

1. **Report Bugs**: Open an issue for any bugs or problems you encounter.
2. **Suggest Features**: Have an idea for improvement? Let us know by opening an issue.
3. **Submit Pull Requests**: Fork the repository, make your changes, and submit a pull request for review.

Make sure to follow the existing coding style and include comments explaining any new features.

---

## License

This project is licensed under the [MIT License](./LICENSE). You are free to use, modify, and distribute this project as long as the original copyright notice is included.

---

## Disclaimer

This project is provided **as-is** without any warranties. It is designed for personal use and educational purposes only. By using this project, you are responsible for ensuring its compliance with applicable laws and website terms of service. The authors assume no liability for any misuse.