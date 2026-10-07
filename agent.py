import os
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.prebuilt import create_react_agent

# Import your custom tools
from agent.tools import get_supplier_history, retrieve_quality_guidelines, analyze_quality_report
from config import GEMINI_MODEL

load_dotenv()

class LangGraphExecutor:
    def __init__(self):
        # 1. Initialize Gemini 3.8 Flash
        self.llm = ChatGoogleGenerativeAI(model=GEMINI_MODEL, temperature=0.1)
        
        # 2. Define Tools
        self.tools = [get_supplier_history, retrieve_quality_guidelines, analyze_quality_report]
        
        # 3. Create the LangGraph Agent (No fragile keyword arguments)
        self.agent_app = create_react_agent(self.llm, self.tools)

        # 4. Save the System Prompt to be used during invocation
        self.system_prompt = SystemMessage(content="""
        You are AgriQuality Copilot, an expert AI decision assistant for agricultural procurement.
        You evaluate commodity lots to recommend whether to ACCEPT, REJECT, or RETEST them.
        
        WORKFLOW:
        1. Use 'retrieve_quality_guidelines' to find rules for the specified commodity.
        2. Use 'analyze_quality_report' to deterministically evaluate the exact parameters. DO NOT do the math yourself.
        3. Use 'get_supplier_history' to check if the supplier's trend impacts the decision.
        
        OUTPUT FORMAT:
        You MUST output your final answer strictly as a valid JSON object matching this schema. Do not include markdown blocks or text outside the JSON:
        {
            "recommendation": "ACCEPT" | "REJECT" | "RETEST",
            "risk_level": "LOW" | "MEDIUM" | "HIGH",
            "reasons": ["Reason 1", "Reason 2"],
            "evidence": ["Evidence from RAG", "Evidence from Supplier history"],
            "next_action": "Actionable next step"
        }
        """)

    def invoke(self, inputs: dict) -> dict:
        user_input = inputs["input"]
        
        # Pass the System Prompt AND User Input directly into the LangGraph state
        initial_state = {
            "messages": [
                self.system_prompt, 
                HumanMessage(content=user_input)
            ]
        }
        
        # Stream the graph execution to the terminal for debugging
        print("\n--- LangGraph Execution Started ---")
        final_state = None
        
        for step in self.agent_app.stream(initial_state, stream_mode="values"):
            latest_message = step["messages"][-1]
            # Safely get content for printing
            content = latest_message.content if isinstance(latest_message.content, str) else str(latest_message.content)
            print(f"[{latest_message.type.upper()}]: {content[:200]}...")
            final_state = step
            
        print("--- LangGraph Execution Finished ---\n")
        
        # The final output is the content of the very last message in the state
        final_message_content = final_state["messages"][-1].content
        if isinstance(final_message_content, list):
            final_message_content = final_message_content[0].get("text", "")
            
        return {"output": str(final_message_content)}

def get_agent_executor():
    return LangGraphExecutor()