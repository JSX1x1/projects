# Robots.txt Checker

## Description
A simple tool for checking the contents of a website's `robots.txt` file. This project is a combination of a Flask backend (Python) and a front-end (HTML, CSS, JavaScript) interface. It allows users to input a URL, fetch the `robots.txt` file from the given site, and display it in a formatted and readable way.

## Legal Disclaimer

**Disclaimer of Liability:**  
This project is for educational purposes only. The use of the `robots.txt` checker should be done in accordance with the website's terms of service. This tool is designed to scrape publicly available data (robots.txt) and should not be used for any unauthorized or unethical scraping activities. The creators of this tool do not take responsibility for any legal issues or violations that may arise from improper use of this tool.

By using this tool, you agree to comply with all relevant laws and website terms of service.

**Note:** Always ensure that you have proper authorization before scraping any website and respect any limitations specified in the `robots.txt` file.

## Setup Instructions

This project consists of two parts: the **Flask backend** (Python) and the **frontend** (HTML, CSS, JavaScript). Below are the setup instructions for both components.

### Requirements

- Python 3.7+
- Flask (`Python`)
- Requests (`Python`)
- Web Browser (for accessing the frontend)

### 1. Python (Flask Backend) Setup

#### Step 1: Install Dependencies

1. First, make sure you have Python 3.7+ installed. You can download it from [here](https://www.python.org/downloads/).
   
2. Install the required Python libraries by running the following command:

   ```bash
   pip install Flask requests
   ```

#### Step 2: Running the Flask Server

1. In your terminal or command prompt, navigate to the directory containing your `app.py` and `index.html` files.

2. Run the Flask server by executing:

   ```bash
   python app.py
   ```

3. The Flask application will start running locally on `http://127.0.0.1:5000/`. Open this URL in a web browser to use the tool.

#### Step 3: Flask Server Code (`app.py`)

- The `app.py` file starts the Flask server and serves the `index.html` file for the frontend. It also handles the `/get-robots` route to fetch the `robots.txt` file for the provided URL.

---

### 2. Frontend Setup (HTML, CSS, JavaScript)

The HTML frontend interacts with the Flask backend to fetch and display the `robots.txt` content.

#### Step 1: Set Up the Frontend

1. Save the `index.html` content as `index.html` in the same directory as `app.py`.
2. The frontend is designed using simple HTML, CSS, and JavaScript. It features an input field for the URL, a button to trigger the fetch, and a textarea to display the `robots.txt` file.

---

## How to Use

1. **Launch the Server**: After setting up the Flask backend, run `python app.py` to start the server.
   
2. **Open the Web App**: Open a web browser and navigate to `http://127.0.0.1:5000/`.

3. **Enter the URL**: On the web page, you'll see an input field labeled **"Enter website URL (e.g., https://example.com)"**. Type the URL of the website you'd like to check.

4. **Check robots.txt**: After entering the URL, click the **"Check robots.txt"** button. The application will:
   - Send a request to the Flask server to fetch the `robots.txt` file from the given URL.
   - If the file is found, its content will be displayed in a read-only textarea.
   - If there’s an error (e.g., the file is not found, the URL is incorrect, etc.), an error message will appear.

5. **View Explanation**: Once the `robots.txt` content is displayed, you can see an explanation of the most common rules:
   - **User-agent**: Refers to the specific web crawlers or bots affected by the rules.
   - **Disallow**: Tells which parts of the site should not be crawled.
   - **Allow**: Tells which parts of the site can be crawled.

---

## What It Does

- **Checks robots.txt**: This tool fetches and displays the contents of the `robots.txt` file from a specified URL.
- **Hacker-style UI**: The front-end interface is designed with a "hacker" terminal theme, featuring dark background and green text.
- **Explanation**: Provides basic explanations of the `robots.txt` directives like `User-agent`, `Disallow`, and `Allow`.
- **Error Handling**: Displays error messages if the `robots.txt` file is not found or if there is a problem fetching it.

---

## Example

1. **Enter URL**:  
   For example, entering `https://example.com` will attempt to fetch the `robots.txt` file from `https://example.com/robots.txt`.

2. **Output**:
   If the file exists, the content will be displayed, followed by an explanation of the rules, such as:

   ```
   User-agent: *
   Disallow: /private/
   Allow: /public/
   ```

   This would indicate that all bots (`User-agent: *`) are blocked from accessing `/private/` but allowed to access `/public/`.

---

## Additional Features

- **AJAX Interaction**: The frontend uses JavaScript with AJAX to fetch the `robots.txt` file asynchronously, making the user experience seamless.
- **Error Handling**: The application provides error messages for various cases, such as invalid URLs or inaccessible `robots.txt` files.
- **Responsive Design**: The interface adapts to different screen sizes, making it user-friendly on both desktops and mobile devices.

---

## Troubleshooting

### 1. **Flask Server Not Running**:
   If you are unable to access the app at `http://127.0.0.1:5000/` after starting the Flask server, make sure that there are no errors in the terminal. The server must be running without issues for the frontend to work.

### 2. **URL Errors**:
   If you input an invalid URL or if the website doesn’t have a `robots.txt` file, the application will display an appropriate error message.

---

## Contributing

If you'd like to contribute to this project, feel free to fork it, submit issues, or open pull requests for improvements.

---

## Acknowledgements

- **Flask**: A micro web framework used for creating the backend server.
- **Requests**: A Python library for making HTTP requests.
- **HTML, CSS, JavaScript**: For creating the interactive frontend interface.