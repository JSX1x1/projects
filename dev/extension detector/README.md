# Browser Extension Detection Script

This JavaScript script allows users to detect active browser extensions running in their own browser. It scans for known extension signatures, such as specific global variables, injected content, modified network activity, and more.

## Purpose

This script is designed for **personal use only**. It helps users identify extensions running in their own browser to better understand their security and privacy. The script should not be used for monitoring or interacting with other users' browsers.

## Features

- Detects common extensions like **AdBlock**, **Grammarly**, **Ghostery**, **Tampermonkey**, and more.
- Checks for injected scripts and styles that may indicate active extensions.
- Scans for changes in network activity and local storage used by extensions.
- Detects any embedded content or iframes injected by extensions.

## How to Use

1. Open the **Developer Tools** in your browser (right-click -> Inspect or press `Ctrl+Shift+I` / `Cmd+Option+I`).
2. Go to the **Console** tab.
3. Copy and paste the entire script into the console and press Enter.
4. Check the console output for detected extensions.

## Ethical Guidelines

- **For personal use only**: This tool is intended for **personal security** and **educational purposes**. Use it only on your own browser to check for extensions running on your system.
- **Do not use on third-party websites**: Do not inject this script into websites you do not own or do not have permission to test, as it could violate terms of service and privacy regulations.