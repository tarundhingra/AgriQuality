import json
from langchain_core.tools import tool
from config import SUPPLIERS_FILE
from rag.retriever import get_retriever

@tool
def get_supplier_history(supplier_name: str) -> str:
    """Fetches historical performance data and quality trends for a given supplier."""
    try:
        with open(SUPPLIERS_FILE, "r") as f:
            suppliers = json.load(f)
        for s in suppliers:
            if s["supplier_name"].lower() == supplier_name.lower():
                return json.dumps(s, indent=2)
        return f"Supplier '{supplier_name}' not found in database. Treat as NEW supplier."
    except Exception as e:
        return f"Error reading supplier data: {str(e)}"

@tool
def retrieve_quality_guidelines(query: str) -> str:
    """Retrieves official agricultural quality standards and rules based on commodity and parameter."""
    retriever = get_retriever()
    docs = retriever.invoke(query)
    if not docs:
        return "No relevant guidelines found."
    return "\n".join([doc.page_content for doc in docs])

@tool
def analyze_quality_report(commodity: str, moisture: float, protein: float, broken_grains: float, foreign_matter: float) -> str:
    """
    Deterministic Python logic to evaluate raw numerical quality parameters.
    The LLM MUST use this tool instead of guessing numerical thresholds.
    """
    commodity = commodity.lower()
    results = {}

    if commodity == "wheat":
        results["moisture"] = "above_preferred_range" if moisture > 12.0 else "within_range"
        results["protein"] = "below_preferred_range" if protein < 11.0 else "within_range"
        results["broken_grains"] = "above_limit" if broken_grains > 5.0 else "within_range"
        results["foreign_matter"] = "above_limit" if foreign_matter > 1.0 else "within_range"
    elif commodity == "rice":
        results["moisture"] = "above_limit" if moisture > 14.0 else "within_range"
        results["broken_grains"] = "above_premium_limit" if broken_grains > 5.0 else "within_range"
        results["foreign_matter"] = "above_limit" if foreign_matter > 0.5 else "within_range"
    else:
        results["status"] = "No deterministic rules configured for this commodity. Rely entirely on RAG guidelines."

    return json.dumps(results, indent=2)