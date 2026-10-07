import streamlit as st
import json
from dotenv import load_dotenv
from agent.agent import get_agent_executor

load_dotenv()

st.set_page_config(page_title="AgriQuality Copilot", layout="wide")

st.title("🌾 AgriQuality Copilot")
st.subheader("Agentic Food Quality & Procurement Decision Assistant")
st.markdown("---")

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### Lot Details")
    lot_id = st.text_input("Lot ID", value="W-104")
    commodity = st.selectbox("Commodity", ["Wheat", "Rice", "Maize"])
    supplier = st.text_input("Supplier Name", value="ABC Traders")
    
    st.markdown("### Quality Parameters")
    moisture = st.number_input("Moisture (%)", value=14.2, step=0.1)
    protein = st.number_input("Protein (%)", value=10.8, step=0.1)
    broken_grains = st.number_input("Broken grains (%)", value=5.1, step=0.1)
    foreign_matter = st.number_input("Foreign matter (%)", value=1.2, step=0.1)
    
    analyze_btn = st.button("Analyze Lot", type="primary", use_container_width=True)

with col2:
    if analyze_btn:
        with st.spinner("Agent is retrieving guidelines, querying supplier history, and calculating parameters..."):
            agent = get_agent_executor()
            prompt = f"""
            Analyze this lot:
            Lot ID: {lot_id}
            Commodity: {commodity}
            Supplier: {supplier}
            Moisture: {moisture}%
            Protein: {protein}%
            Broken grains: {broken_grains}%
            Foreign matter: {foreign_matter}%
            """
            
            try:
                response = agent.invoke({"input": prompt})
                output_str = response["output"].strip()
                
                # Clean up potential markdown formatting from LLM
                if output_str.startswith("```json"):
                    output_str = output_str[7:-3]
                elif output_str.startswith("```"):
                    output_str = output_str[3:-3]
                    
                decision = json.loads(output_str)
                
                # Render UI
                st.markdown(f"## Recommendation: **{decision['recommendation']}**")
                
                risk_color = "green" if decision['risk_level'] == "LOW" else "orange" if decision['risk_level'] == "MEDIUM" else "red"
                st.markdown(f"**Risk Level:** :{risk_color}[{decision['risk_level']}]")
                
                st.markdown("### Why?")
                for reason in decision['reasons']:
                    st.markdown(f"- {reason}")
                    
                st.markdown("### Retrieved Evidence")
                for ev in decision['evidence']:
                    st.markdown(f"- *{ev}*")
                    
                st.info(f"**Recommended Action:** {decision['next_action']}")
                
            except json.JSONDecodeError:
                st.error("The agent returned an invalid response format. Please try again.")
                with st.expander("Show raw output"):
                    st.write(response["output"])
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

# Optional Chat Section
st.markdown("---")
st.markdown("### 💬 Ask Copilot")
chat_input = st.text_input("Ask a follow-up question about this lot, supplier, or quality standards:")
if chat_input:
    with st.spinner("Thinking..."):
        agent = get_agent_executor()
        chat_prompt = f"The user asks: {chat_input}. Answer contextually using your tools. Do not output JSON this time, just plain text."
        response = agent.invoke({"input": chat_prompt})
        st.write(response["output"])