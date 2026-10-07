# 🌾 AgriQuality Copilot — Agentic Food Quality Decision Assistant

> **Disclaimer:** This is an independent AI engineering portfolio project inspired by real-world agricultural quality and procurement workflows (similar to those handled by agritech companies like AGNEXT). It has **no official affiliation** with AGNEXT or any other agricultural entity. All data, supplier histories, and quality standards within this application are synthetic demonstrations created for educational purposes.

## 📖 Project Overview
AgriQuality Copilot is an AI-powered agentic assistant designed to help agricultural procurement executives make data-driven decisions on commodity lots. Given a laboratory quality report (e.g., moisture, protein, foreign matter), the agent evaluates the lot and outputs a structured recommendation to **ACCEPT**, **REJECT**, or **RETEST**.

## 🛑 The Problem Statement
In agricultural procurement, quality control executives evaluate hundreds of commodity lots daily. Making a purchasing decision requires:
1. Checking current lot metrics against strict industry/regulatory guidelines.
2. Performing mathematical comparisons to identify out-of-bounds parameters.
3. Reviewing the supplier's historical reliability.

**Why it matters:** Human error or fatigue can lead to accepting a lot with dangerous moisture levels (risking fungal growth in storage) or rejecting a good lot. A standard chatbot is unreliable here because Large Language Models (LLMs) are notorious for "hallucinating" math and making up numerical rules. 

**The Solution:** This project uses an **Agentic Workflow** where the LLM does not perform the math itself. Instead, it acts as a reasoning engine that calls deterministic Python tools, queries local databases, and retrieves rules using RAG before making a final structured decision.

---

## 🏗️ Architecture & Tech Stack
- **Language:** Python
- **LLM:** Google Gemini 3.8 Flash (Optimized for fast tool-calling)
- **Agent Framework:** LangGraph / LangChain Core
- **Knowledge Base (RAG):** ChromaDB, LangChain Text Splitters & Embeddings
- **Frontend:** Streamlit
- **Data Layer:** Synthetic JSON (No SQL to maintain simplicity and explainability)
- **Data Validation:** Pydantic

---

## ⚙️ How the Agentic Workflow Works
This is not a basic RAG chatbot. It utilizes **LangGraph** to create a cyclic state graph where the LLM reasons and interacts with custom tools until it gathers enough evidence to formulate a decision.

### 1. The Tool-Calling Workflow
When a user submits a lot, the Gemini model evaluates the request and dynamically routes to the following tools:
*   `retrieve_quality_guidelines`: Uses a ChromaDB Retriever to fetch the exact guidelines for the specified commodity.
*   `analyze_quality_report`: A deterministic Python function that evaluates the numerical parameters. *The LLM is strictly forbidden from doing math—it must pass the numbers to this tool to prevent hallucinated measurements.*
*   `get_supplier_history`: Queries the synthetic JSON database to fetch the supplier's historical acceptance rate and recent quality trends.

### 2. The Final Decision
Once the agent gathers the outputs from these tools, it compiles the evidence into a strict JSON schema that Streamlit parses to display a highly readable dashboard.

---

## 🚀 Setup Instructions

### 1. Clone the repository and navigate to the directory
```bash
git clone [https://github.com/yourusername/agriquality-copilot.git](https://github.com/yourusername/agriquality-copilot.git)
cd agriquality-copilot
2. Create a Virtual Environment
Bash
python -m venv env
# Windows
.\env\Scripts\activate
# Mac/Linux
source env/bin/activate
3. Install Dependencies
Bash
python -m pip install --upgrade pip
pip install -r requirements.txt
4. Setup Environment Variables
Create a .env file in the root directory and add your Google Gemini API key:

Code snippet
GEMINI_API_KEY=your_actual_api_key_here
5. Initialize the Vector Database (RAG)
Run the ingestion script once to load the synthetic guidelines into ChromaDB.

Bash
python rag/ingest.py
6. Run the Application
Bash
streamlit run app.py
📸 Example Inputs & Outputs
Example Input:

Lot ID: W-104

Commodity: Wheat

Supplier: ABC Traders

Moisture: 14.2%

Protein: 10.8%

Expected Output (Agentic Decision):

Recommendation: REJECT

Risk Level: HIGH

Why? Moisture is dangerously above the 12.0% safe limit. Protein is below the preferred range.

Retrieved Evidence: "Moisture above 14.0% is highly dangerous for storage."

Actionable Step: Reject the lot and notify ABC Traders of the moisture violation.


⚠️ Limitations & Future Improvements
No Real Database: Currently uses flat JSON files for explainability. A production version would integrate PostgreSQL or a data warehouse.

Static Thresholds: The deterministic Python tool uses static thresholds. In production, these would be dynamically pulled from a live regulatory database.

No Computer Vision: Currently relies on manually entered lab reports. A future iteration could integrate Gemini Vision to process photos of the grain samples directly.
