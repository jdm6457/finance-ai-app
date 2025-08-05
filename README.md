# AI-Powered Personal Finance Dashboard

This project is a self-hosted, privacy-focused personal finance application designed to provide a unified view of financial accounts and deliver intelligent insights through a multi-agent AI system. The entire platform runs locally using Docker, ensuring that all sensitive financial data remains under the user's control.

## Security Notice

**This repository contains only source code.** For security and privacy, all sensitive information is explicitly excluded via the `.gitignore` file. This includes:
* **Credentials:** API keys, usernames, and passwords.
* **Session Data:** Saved login sessions that could be used to access accounts.
* **Personal Data:** Any downloaded financial data.
* **Large Files:** Downloaded AI models.

Anyone cloning this repository will need to provide their own credentials and generate their own session files to run the application.

## Current Status: Phase 2 In Progress (Data Acquisition)

### Phase 1: Environment Setup (Complete)
The foundational environment for the application has been successfully built, configured, and verified. All core services are running within a Docker Compose setup, including a custom Python-enabled n8n image with GPU acceleration for the local Ollama LLM.

### Phase 2: Data Acquisition (In Progress)

#### AssetMark Scraper (Complete)
The first data pipeline has been successfully built for AssetMark accounts.
* **Technology:** The scraper is a Python script using the Playwright library for browser automation.
* **MFA Handling:** The script uses a robust two-stage process to handle Multi-Factor Authentication (MFA) securely:
    1.  **Manual Authentication (`--auth`):** A one-time, headed browser session is launched, allowing the user to log in, complete the MFA challenge, and check the "remember this device for 90 days" box. The script then saves the resulting session state (cookies and tokens) to a secure local file.
    2.  **Automated Execution:** For daily runs, the script runs headlessly, loads the saved session file, and bypasses the login/MFA steps entirely, proceeding directly to the account dashboard to scrape the data.

#### Schwab API Integration (Pending)
Waiting for developer API key approval from Schwab. Once approved, an OAuth 2.0 client will be built to fetch brokerage account data.

## Developer Notes & Troubleshooting

Setting up a complex, multi-service local environment presents several challenges. This project overcame the following issues, which may be helpful for others:

* **Docker Image Incompatibility:** The standard Alpine-based n8n Docker image lacked the necessary build tools for the Python Playwright library. The solution was to build a custom image from a more robust `debian:bullseye-slim` base.
* **GUI Forwarding for Headed Scraping:** To run the one-time manual authentication for the scraper, a graphical browser window needed to be displayed from within the Linux Docker container on a Windows desktop. This was solved by:
    1.  Installing and configuring **VcXsrv** on Windows, ensuring the "Disable access control" option was checked.
    2.  Creating a **Windows Firewall rule** to allow inbound connections on ports 6000-6003.
    3.  Passing the `DISPLAY` environment variable to the container. The reliable method for this setup was to use the Docker network gateway IP (e.g., `export DISPLAY=172.19.0.1:0.0`).
* **Advanced Web Scraping Challenges:** The target website was a modern single-page application that presented several race conditions. The final, successful scraping script required:
    1.  **Precise Selectors:** Using highly specific XPath selectors (`//div[text()='...']`) was necessary to uniquely identify elements, as auto-generated CSS class names were unreliable.
    2.  **Multi-Stage Waiting:** The script had to first wait for the page URL to change, then wait for all background network activity to cease (`networkidle`), and *then* wait for a specific, stable element to appear before it could reliably scrape the data.

## Future Enhancements & Roadmap

* **Phase 2 Completion:**
    * Build the Schwab API client.
    * Build scrapers for the Schwab 401(k) portal and Chase banking.
    * Create a data normalization script.
* **Phase 3: Backend & AI Orchestration:**
    * Integrate a PostgreSQL database.
    * Build a master n8n workflow to orchestrate the entire data pipeline.
    * Develop the multi-agent AI system for financial analysis.
* **Phase 4: Frontend Development:**
    * Build a responsive web dashboard using React or a similar framework.
    * Create data visualizations and an interactive chat interface for the AI.