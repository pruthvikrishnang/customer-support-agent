# 🚢 Shipping Customer Support Workflow Agent

Welcome to the **Shipping Customer Support Workflow Agent**! This project implements a graph-based customer support assistant for a shipping company, built using **ADK 2.0 (Agent Development Kit)** and managed via **Agents CLI**.

The agent is designed to run locally, classify customer questions, and route them dynamically to the appropriate response node.

---

## 📐 Agent Architecture

The agent uses a graph-based workflow topology to process user requests:

```
          [START] (User query)
             │
             ▼
      [classifier] (Silent LLM categorization)
             │
             ▼
          [router] (Dynamic Route Fork)
           ├─── "shipping" ───► [shipping_faq_agent] (Playful Support Chat)
           └─── "unrelated" ──► [decline_node] (Polite Out-of-Scope decline)
```

1. **`classifier`**: A silent custom function node utilizing `gemini-flash-latest` with a structured Pydantic schema to determine if the query is related to shipping (rates, tracking, delivery, returns).
2. **`router`**: Inspects the classifier's classification and splits the route.
3. **`shipping_faq_agent`**: A highly enthusiastic, playful chat agent loaded with emojis that answers shipping questions (and highlights the **FREE shipping threshold for orders over $50**!).
4. **`decline_node`**: A static fallback node that politely declines to answer non-shipping questions.

---

## 🚀 Setup Instructions

Follow these easy steps to get your agent up and running locally.

### 1. Clone the Repository
First, clone the repository to your local machine and navigate into the project directory:
```bash
git clone https://github.com/pruthvikrishnang/customer-support-agent.git
cd customer-support-agent
```

### 2. Prerequisites
Ensure you have the following installed on your system:
*   [Python 3.11+](https://www.python.org/)
*   [uv](https://docs.astral.sh/uv/getting-started/installation/) (fast Python package manager)
*   [Node.js 18+](https://nodejs.org/) (required by skills)

### 2. Environment Variables & API Key
This agent queries the Gemini model. You need to configure a Gemini API Key:
1. Copy the `.env.example` file to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and replace `"Put your API key here"` with your actual Google AI Studio API key:
   ```env
   GEMINI_API_KEY="AIzaSy..."
   ```

### 3. Install CLI & Skills
Run the setup command to install `google-agents-cli` and the coding skills:
```bash
uvx google-agents-cli setup
```

### 4. Install Project Dependencies
Sync the python virtual environment and project packages:
```bash
uvx google-agents-cli install
```

## 🎮 Running and Testing

If you have `make` installed on your system, you can use these quick shorthand commands:
*   **Install CLI & skills**: `make setup`
*   **Install dependencies**: `make install`
*   **Run playground server**: `make playground`
*   **Run pytest test suite**: `make test`
*   **Run lint & type checks**: `make lint`

Alternatively, you can execute the raw commands directly:

### A. Run Interactive Playground (Web UI)
Launch the local web playground to interactively chat with your agent:
```bash
uv run adk web . --host 127.0.0.1 --port 8080
```
Open your browser and navigate to:
👉 **[http://127.0.0.1:8080/dev-ui/?app=app](http://127.0.0.1:8080/dev-ui/?app=app)**

#### **🛑 Stopping the Server**
To stop the playground server at any time, simply return to your terminal and press:
*   `Ctrl + C` (on Windows/macOS/Linux)

---

### B. Run CLI Queries
You can query your agent directly from the terminal without launching the full web UI:

**One-Off Query (Starts and stops temporary server):**
```bash
uvx google-agents-cli run "what are the shipping rates to New York?"
```

**Query Running Playground Server (Faster execution):**
If your playground server is already running on port `8080`, query it directly via:
```bash
uvx google-agents-cli run --url http://127.0.0.1:8080 --mode adk --app-name app "how long does standard delivery take?"
```

---

### C. Run Code Verification & Tests
Ensure code quality, type health, and functionality are pristine:

*   **Run pytest test suite:**
    ```bash
    uv run pytest
    ```
*   **Run linting and type checks:**
    ```bash
    uvx google-agents-cli lint
    ```


## Working Prototype :
1) Asking relevant Question :
<img width="1911" height="987" alt="image" src="https://github.com/user-attachments/assets/e74f648d-4b66-437c-b2b5-2be76877aa35" />


2) Asking irrelevant Question :
<img width="1910" height="982" alt="image" src="https://github.com/user-attachments/assets/557a2afb-dedc-4e27-8024-7f357c875649" />

