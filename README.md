# AI-Powered Personal Finance Dashboard

This project is a self-hosted, privacy-focused personal finance application designed to provide a unified view of financial accounts and deliver intelligent insights through a multi-agent AI system. The entire platform runs locally using Docker, ensuring that all sensitive financial data remains under the user's control.

## Current Status: Phase 1 Complete (Environment Setup)

The foundational environment for the application has been successfully built, configured, and verified. All core services are running within a Docker Compose setup.

**Key Accomplishments:**

* **Containerized Services:** `n8n` and `Ollama` services are fully containerized and orchestrated via `docker-compose`.
* **GPU Acceleration:** The `Ollama` service is configured to leverage an NVIDIA GPU, providing significant performance for local Large Language Model (LLM) inference.
* **Custom Python Environment:** A custom `n8n` Docker image has been built, equipping the workflow automation engine with a full Python environment, including the `Playwright` library for browser automation.
* **Verified Connectivity:** End-to-end tests have confirmed that `n8n` can communicate with the `Ollama` LLM service and can execute Python scripts from within its workflows.
* **Organized Project Structure:** The project has been organized with dedicated directories for custom Docker configurations (`n8n_custom/`) and Python scripts (`scripts/`), following best practices for maintainability and future expansion.

## Future Enhancements & Roadmap

The project will be developed in phases, building upon the current stable foundation.

### Phase 2: Data Acquisition

The immediate next step is to build the data acquisition pipelines.

* **Schwab Integration:** Connect to the official Schwab Trader API using Python to fetch brokerage and 401(k) data. This will involve implementing the OAuth 2.0 authentication flow.
* **Web Scraping:** Develop resilient web scrapers using Python and Playwright for institutions without a public API, such as AssetMark (IRAs) and Chase (banking).
* **Data Normalization:** Create a robust ETL script to transform the raw data from all sources into a unified schema before storing it.

### Phase 3: Backend & AI Orchestration

With data pipelines in place, the focus will shift to the application's intelligence core.

* **Database Integration:** Implement a PostgreSQL database within the Docker environment to store the normalized financial data.
* **n8n Workflow Development:** Build a master orchestration workflow in `n8n` to automate the entire data pipeline: trigger scrapers, run the normalization script, and load data into the database.
* **Multi-Agent AI System:** Develop the Supervisor-Worker AI agent architecture within `n8n` to begin analyzing the stored data.

### Phase 4: Frontend Development

The final phase will be to build the user-facing dashboard.

* **UI/UX:** Develop a modern, responsive web interface using a framework like React or Svelte.
* **Data Visualization:** Integrate a charting library like Recharts to create interactive visualizations for net worth, asset allocation, and spending trends.
* **AI Interaction:** Build a chat interface to allow the user to interact with the AI financial advisor.