#include <iostream>
#include <vector>
#include <string>
#include <curl/curl.h>
#include <json/json.h> // Requires JSON for parsing API response

using namespace std;

// Local blacklist of known malicious URLs
vector<string> blacklist = {
    "malicious.com",
    "phishingsite.net",
    "badwebsite.org"
};

// VirusTotal API Key (Replace with your own key)
const string VIRUSTOTAL_API_KEY = "YOUR_VIRUSTOTAL_API_KEY";

// Function to check if a URL is in the local blacklist
bool isMalicious(string url) {
    for (const string& badUrl : blacklist) {
        if (url.find(badUrl) != string::npos) {
            return true;
        }
    }
    return false;
}

// Callback function for handling API response
size_t WriteCallback(void* contents, size_t size, size_t nmemb, string* output) {
    size_t totalSize = size * nmemb;
    output->append((char*)contents, totalSize);
    return totalSize;
}

// Function to scan a URL using VirusTotal API
bool scanWithVirusTotal(const string& url) {
    CURL* curl = curl_easy_init();
    if (!curl) {
        cerr << "Failed to initialize cURL" << endl;
        return false;
    }

    string apiUrl = "https://www.virustotal.com/api/v3/urls";
    string response;
    string postFields = "url=" + url;

    struct curl_slist* headers = NULL;
    headers = curl_slist_append(headers, ("x-apikey: " + VIRUSTOTAL_API_KEY).c_str());
    headers = curl_slist_append(headers, "Content-Type: application/x-www-form-urlencoded");

    curl_easy_setopt(curl, CURLOPT_URL, apiUrl.c_str());
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, postFields.c_str());
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response);

    CURLcode res = curl_easy_perform(curl);
    curl_easy_cleanup(curl);
    curl_slist_free_all(headers);

    if (res != CURLE_OK) {
        cerr << "cURL error: " << curl_easy_strerror(res) << endl;
        return false;
    }

    // Parse JSON response
    Json::Value jsonData;
    Json::CharReaderBuilder readerBuilder;
    string errors;
    istringstream responseStream(response);
    if (!Json::parseFromStream(readerBuilder, responseStream, &jsonData, &errors)) {
        cerr << "Failed to parse JSON response" << endl;
        return false;
    }

    int maliciousCount = jsonData["data"]["attributes"]["last_analysis_stats"]["malicious"].asInt();
    return maliciousCount > 0;
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        cout << "❌ Usage: " << argv[0] << " <URL>\n";
        return 1;
    }

    string url = argv[1];
    cout << "Scanning URL: " << url << "...\n";

    // 1️⃣ Check local blacklist first
    if (isMalicious(url)) {
        cout << "WARNING! This URL is flagged as MALICIOUS in local blacklist!\n";
        return 0;
    } else {
        cout << "Not found in local blacklist. Checking VirusTotal...\n";
    }

    // 2️⃣ Check with VirusTotal API
    bool isMaliciousOnline = scanWithVirusTotal(url);
    if (isMaliciousOnline) {
        cout << "WARNING! This URL is flagged as MALICIOUS by VirusTotal!\n";
    } else {
        cout << "No known threats detected by VirusTotal.\n";
    }

    return 0;
}
