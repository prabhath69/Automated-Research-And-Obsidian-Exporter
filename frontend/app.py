import streamlit as st
import requests
import time

st.set_page_config(page_title="Agentic Research Synthesizer", layout="wide")

st.title("Automated Research Synthesizer")
st.write("Enter a research query to generate a comprehensive report and export to Obsidian.")

query = st.text_input("Research Query", "How are AI agents being used in supply-chain logistics?")

if st.button("Start Research"):
    with st.spinner("Starting Agentic Workflow..."):
        try:
            response = requests.post("http://127.0.0.1:8000/research", json={"query": query})
            response.raise_for_status()
            data = response.json()
            research_id = data["research_id"]
            
            st.success(f"Research Job Completed! ID: {research_id}")
            
            # Fetch results
            res = requests.get(f"http://127.0.0.1:8000/research/{research_id}")
            res.raise_for_status()
            result = res.json()
            
            st.header("1. Research Plan")
            plan = result.get("research_plan", {})
            st.write(f"**Objective:** {plan.get('main_objective', '')}")
            st.write("**Sub-Questions:**")
            for q in plan.get("sub_questions", []):
                st.write(f"- {q}")
                
            st.header(f"2. Collected Sources ({len(result.get('collected_sources', []))})")
            for source in result.get("collected_sources", []):
                st.write(f"- [{source['source_id']}] {source['title']} ({source['url']})")
                
            st.header("3. Final Report")
            st.markdown(result.get("final_report", "No report generated."))
            
        except Exception as e:
            st.error(f"Error: {e}")
