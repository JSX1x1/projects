import sys
import csv
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QTextEdit, QTableWidget, QTableWidgetItem, QHeaderView, QFileDialog
from PyQt6.QtCore import Qt
import re
import time
from urllib.parse import urlparse

# Blacklist von unsicheren Domains
BLACKLIST = ["example.com", "malicious.com", "phishing.com"]
SPAM_KEYWORDS = ["buy viagra", "free gift", "get rich quick", "loan offer", "investment scam"]
MALICIOUS_SCRIPTS = ["eval(", "document.write(", "alert(", "popup("]

class WebScraperApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ethical Hacker Web Scraper - Advanced")
        self.setStyleSheet("background-color: black; color: green;")

        # Layouts
        layout = QVBoxLayout()

        # Eingabefeld für URL
        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("Enter URL here...")
        self.url_input.setStyleSheet("background-color: #333; color: green; padding: 5px;")
        layout.addWidget(self.url_input)

        # Scrape-Button
        self.scrape_button = QPushButton("Scrape Website", self)
        self.scrape_button.setStyleSheet("background-color: #444; color: green;")
        self.scrape_button.clicked.connect(self.scrape_website)
        layout.addWidget(self.scrape_button)

        # Textbereich für Log-Ausgabe
        self.log_output = QTextEdit(self)
        self.log_output.setReadOnly(True)
        self.log_output.setStyleSheet("background-color: #222; color: green; padding: 5px;")
        layout.addWidget(self.log_output)

        # Table für die Daten
        self.table = QTableWidget(self)
        self.table.setColumnCount(5)  # Titel, Link, Inhalt, Tag, Details
        self.table.setHorizontalHeaderLabels(["Title", "Link", "Content", "Tag", "Details"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        # CSV speichern Button
        self.save_button = QPushButton("Save to CSV", self)
        self.save_button.setStyleSheet("background-color: #444; color: green;")
        self.save_button.clicked.connect(self.save_to_csv)
        layout.addWidget(self.save_button)

        # Set the layout
        self.setLayout(layout)

        self.request_limit = 10  # Max. Anfragen pro Domain
        self.request_count = {}  # Zähler für Anfragen pro Domain

    def check_robots_txt(self, url):
        # Die URL für robots.txt abrufen
        parsed_url = urlparse(url)
        robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"

        try:
            response = requests.get(robots_url)
            if response.status_code == 200:
                return response.text
        except requests.exceptions.RequestException as e:
            self.log_output.append(f"Fehler beim Abrufen der robots.txt: {str(e)}")
        return ""

    def is_allowed(self, url):
        # Prüfe, ob URL in robots.txt erlaubt ist
        robots_txt = self.check_robots_txt(url)
        if "User-agent: *" in robots_txt:
            disallowed_paths = [line.split(":")[1].strip() for line in robots_txt.splitlines() if line.startswith('Disallow')]
            for path in disallowed_paths:
                if url.startswith(path):
                    return False
        return True

    def scrape_website(self):
        url = self.url_input.text().strip()

        if not url:
            self.log_output.append("Please enter a valid URL.")
            return

        self.log_output.append(f"Scraping: {url}...\n")

        # Check if scraping is allowed by robots.txt
        if not self.is_allowed(url):
            self.log_output.append("Scraping is not allowed by robots.txt.")
            return

        # Selenium setup
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run without opening a browser window
        chrome_service = Service("/path/to/chromedriver")  # Specify path to chromedriver

        driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
        driver.get(url)

        # Optional: Warten, damit alle JavaScript-Inhalte geladen werden
        driver.implicitly_wait(5)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Meta-Daten
        title = soup.find('title').get_text() if soup.find('title') else "No Title"
        description = soup.find('meta', attrs={'name': 'description'}) or soup.find('meta', attrs={'property': 'og:description'})
        description = description['content'] if description else "No Description"
        keywords = soup.find('meta', attrs={'name': 'keywords'})
        keywords = keywords['content'] if keywords else "No Keywords"
        author = soup.find('meta', attrs={'name': 'author'})
        author = author['content'] if author else "No Author"

        # Scraping all relevant data (titles, links, text, tags)
        titles = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        links = soup.find_all('a', href=True)
        paragraphs = soup.find_all('p')
        images = soup.find_all('img', src=True)
        tables = soup.find_all('table')
        divs = soup.find_all('div')

        # Analyse der Links und Malicious Content Detection
        malicious_content = False
        malicious_details = []

        # Link-Überprüfung auf schwarze Liste und Spam
        for link in links:
            href = link.get('href', '')
            if any(blacklisted in href for blacklisted in BLACKLIST):
                malicious_content = True
                malicious_details.append(f"Suspicious URL detected: {href}")

            if any(keyword in href.lower() for keyword in SPAM_KEYWORDS):
                malicious_content = True
                malicious_details.append(f"Spam-like URL detected: {href}")

        # Malicious Content Flagging (optional)
        if malicious_content:
            self.log_output.append("Malicious content detected:\n")
            for detail in malicious_details:
                self.log_output.append(f"- {detail}")
        else:
            self.log_output.append("No malicious content detected.\n")

        # Add data to the table
        self.table.setRowCount(0)  # Reset the table
        for idx, title_tag in enumerate(titles, start=1):
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)

            # Title
            self.table.setItem(row_position, 0, QTableWidgetItem(title_tag.get_text(strip=True)))

            # Link (if any)
            link = title_tag.find_parent('a')['href'] if title_tag.find_parent('a') else ''
            self.table.setItem(row_position, 1, QTableWidgetItem(link))

            # Content (extract text from paragraphs)
            content = "\n".join([p.get_text(strip=True) for p in paragraphs])
            self.table.setItem(row_position, 2, QTableWidgetItem(content[:100] + "..."))

            # Tag (for demo purposes, we display the tag name)
            self.table.setItem(row_position, 3, QTableWidgetItem(str(title_tag.name)))

            # Details (e.g. src for images)
            img_src = ", ".join([img['src'] for img in images]) if images else "No Images"
            self.table.setItem(row_position, 4, QTableWidgetItem(img_src))

        # Log Output
        self.log_output.append(f"Meta Information:\nTitle: {title}\nDescription: {description}\nKeywords: {keywords}\nAuthor: {author}\n")
        self.log_output.append(f"Scraping completed.\n")

        # Close the Selenium driver
        driver.quit()

        # Implement pause to avoid hitting rate limits
        time.sleep(3)

    def save_to_csv(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save CSV", "", "CSV Files (*.csv)")

        if filename:
            try:
                with open(filename, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Title", "Link", "Content", "Tag", "Details"])

                    # Loop through the table and write data to CSV
                    for row in range(self.table.rowCount()):
                        row_data = []
                        for col in range(self.table.columnCount()):
                            row_data.append(self.table.item(row, col).text())
                        writer.writerow(row_data)

                self.log_output.append(f"Data saved to CSV: {filename}\n")
            except Exception as e:
                self.log_output.append(f"Error saving to CSV: {str(e)}\n")

# Start the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WebScraperApp()
    window.show()
    sys.exit(app.exec())
