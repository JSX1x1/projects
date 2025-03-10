#include <QApplication>
#include <QWidget>
#include <QVBoxLayout>
#include <QPushButton>
#include <QLineEdit>
#include <QTextEdit>
#include <QTableWidget>
#include <QTableWidgetItem>
#include <QHeaderView>
#include <QFileDialog>
#include <curl/curl.h>
#include <gumbo.h>
#include <QMessageBox>
#include <QTime>

// Blacklist and spam-related keywords
const std::vector<std::string> BLACKLIST = {"example.com", "malicious.com", "phishing.com"};
const std::vector<std::string> SPAM_KEYWORDS = {"buy viagra", "free gift", "get rich quick", "loan offer", "investment scam"};

// Function to handle HTTP requests using libcurl
size_t WriteCallback(void* contents, size_t size, size_t nmemb, void* userp) {
    ((std::string*)userp)->append((char*)contents, size * nmemb);
    return size * nmemb;
}

std::string fetch_html(const std::string& url) {
    CURL* curl;
    CURLcode res;
    std::string readBuffer;

    curl_global_init(CURL_GLOBAL_DEFAULT);
    curl = curl_easy_init();
    if(curl) {
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);
        res = curl_easy_perform(curl);
        if(res != CURLE_OK)
            fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));
        curl_easy_cleanup(curl);
    }
    curl_global_cleanup();
    return readBuffer;
}

// Function to parse HTML content with Gumbo
void parse_html(const std::string& html, std::vector<std::string>& titles, std::vector<std::string>& links, std::vector<std::string>& paragraphs) {
    GumboOutput* output = gumbo_parse(html.c_str());
    GumboVector* root_children = &output->root->v.element.children;
    
    for (unsigned i = 0; i < root_children->length; ++i) {
        GumboNode* child = static_cast<GumboNode*>(root_children->data[i]);
        if (child->type == GUMBO_NODE_ELEMENT) {
            GumboElement* element = &child->v.element;
            if (element->tag == GUMBO_TAG_H1 || element->tag == GUMBO_TAG_H2 || element->tag == GUMBO_TAG_H3) {
                titles.push_back(gumbo_get_text(child));  // Get title text
            }
            if (element->tag == GUMBO_TAG_A) {
                GumboAttribute* href = gumbo_get_attribute(&element->attributes, "href");
                if (href) links.push_back(href->value);  // Get link
            }
            if (element->tag == GUMBO_TAG_P) {
                paragraphs.push_back(gumbo_get_text(child));  // Get paragraph text
            }
        }
    }
    gumbo_destroy_output(&kGumboDefaultOptions, output);
}

// GUI Class for Web Scraper
class WebScraperApp : public QWidget {
    Q_OBJECT
public:
    WebScraperApp(QWidget *parent = nullptr) : QWidget(parent) {
        setWindowTitle("Ethical Hacker Web Scraper - Advanced");
        setStyleSheet("background-color: black; color: green;");
        
        QVBoxLayout *layout = new QVBoxLayout(this);

        // URL Input
        url_input = new QLineEdit(this);
        url_input->setPlaceholderText("Enter URL here...");
        url_input->setStyleSheet("background-color: #333; color: green; padding: 5px;");
        layout->addWidget(url_input);

        // Scrape Button
        scrape_button = new QPushButton("Scrape Website", this);
        scrape_button->setStyleSheet("background-color: #444; color: green;");
        layout->addWidget(scrape_button);

        connect(scrape_button, &QPushButton::clicked, this, &WebScraperApp::scrapeWebsite);

        // Log Output
        log_output = new QTextEdit(this);
        log_output->setReadOnly(true);
        log_output->setStyleSheet("background-color: #222; color: green; padding: 5px;");
        layout->addWidget(log_output);

        // Table for Results
        table = new QTableWidget(this);
        table->setColumnCount(5);
        table->setHorizontalHeaderLabels({"Title", "Link", "Content", "Tag", "Details"});
        table->horizontalHeader()->setSectionResizeMode(QHeaderView::Stretch);
        layout->addWidget(table);

        // Save to CSV Button
        save_button = new QPushButton("Save to CSV", this);
        save_button->setStyleSheet("background-color: #444; color: green;");
        layout->addWidget(save_button);
        connect(save_button, &QPushButton::clicked, this, &WebScraperApp::saveToCSV);

        setLayout(layout);
    }

private slots:
    void scrapeWebsite() {
        std::string url = url_input->text().toStdString();

        if (url.empty()) {
            log_output->append("Please enter a valid URL.");
            return;
        }

        log_output->append(QString("Scraping: %1...").arg(url.c_str()));

        // Fetch the HTML content of the website
        std::string html = fetch_html(url);
        if (html.empty()) {
            log_output->append("Failed to retrieve HTML.");
            return;
        }

        // Parse HTML content to extract titles, links, and paragraphs
        std::vector<std::string> titles, links, paragraphs;
        parse_html(html, titles, links, paragraphs);

        // Populate table with extracted data
        table->setRowCount(0);
        for (size_t i = 0; i < titles.size(); ++i) {
            table->insertRow(i);
            table->setItem(i, 0, new QTableWidgetItem(QString::fromStdString(titles[i])));
            table->setItem(i, 1, new QTableWidgetItem(QString::fromStdString(links[i])));
            table->setItem(i, 2, new QTableWidgetItem(QString::fromStdString(paragraphs[i])));
            table->setItem(i, 3, new QTableWidgetItem("Tag"));  // Simplified; real tags are more complex
            table->setItem(i, 4, new QTableWidgetItem("Details"));
        }

        log_output->append("Scraping completed.");
    }

    void saveToCSV() {
        QString filename = QFileDialog::getSaveFileName(this, "Save CSV", "", "CSV Files (*.csv)");
        if (filename.isEmpty()) return;

        QFile file(filename);
        if (file.open(QIODevice::WriteOnly)) {
            QTextStream stream(&file);
            stream << "Title,Link,Content,Tag,Details\n";
            for (int row = 0; row < table->rowCount(); ++row) {
                for (int col = 0; col < table->columnCount(); ++col) {
                    stream << table->item(row, col)->text();
                    if (col < table->columnCount() - 1) stream << ",";
                }
                stream << "\n";
            }
            log_output->append("Data saved to CSV.");
        }
    }

private:
    QLineEdit *url_input;
    QPushButton *scrape_button;
    QTextEdit *log_output;
    QTableWidget *table;
    QPushButton *save_button;
};

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);

    WebScraperApp window;
    window.show();

    return app.exec();
}

