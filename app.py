"""
AI Agent Debugger - Streamlit Version
"""

import streamlit as st
import time

st.set_page_config(page_title="AI Agent Debugger", page_icon="🤖")

st.title("🤖 AI Agent Debugger")
st.markdown("Visual debugging tool for multi-agent AI systems")

# Initialize session state
if 'agents' not in st.session_state:
    st.session_state.agents = {
        "intake": {"status": "idle", "calls": 0, "latency": 0.3},
        "validator": {"status": "idle", "calls": 0, "latency": 0.5},
        "processor": {"status": "idle", "calls": 0, "latency": 0.8},
        "responder": {"status": "idle", "calls": 0, "latency": 0.4}
    }
    st.session_state.log = []

query = st.text_input("Enter your query:", placeholder="e.g., 'Process order #12345'")

if st.button("🔍 Trace Execution", type="primary"):
    if query:
        st.session_state.log = []
        
        # Simulate agent execution
        with st.spinner("Running agents..."):
            # Intake Agent
            st.session_state.agents["intake"]["status"] = "processing"
            st.session_state.agents["intake"]["calls"] += 1
            time.sleep(0.3)
            st.session_state.log.append({
                "agent": "Intake Agent",
                "input": query,
                "output": f"Parsed: '{query}'",
                "latency": 0.3,
                "status": "✅"
            })
            st.session_state.agents["intake"]["status"] = "idle"
            
            # Validator Agent
            st.session_state.agents["validator"]["status"] = "processing"
            st.session_state.agents["validator"]["calls"] += 1
            time.sleep(0.5)
            is_valid = len(query) > 5
            st.session_state.log.append({
                "agent": "Validator Agent", 
                "input": f"Parsed: '{query}'",
                "output": f"Valid: {is_valid}",
                "latency": 0.5,
                "status": "✅" if is_valid else "❌"
            })
            st.session_state.agents["validator"]["status"] = "idle"
            
            if is_valid:
                # Processor Agent
                st.session_state.agents["processor"]["status"] = "processing"
                st.session_state.agents["processor"]["calls"] += 1
                time.sleep(0.8)
                result = f"Processed: '{query}'"
                st.session_state.log.append({
                    "agent": "Processor Agent",
                    "input": f"Valid: {is_valid}",
                    "output": result,
                    "latency": 0.8,
                    "status": "✅"
                })
                st.session_state.agents["processor"]["status"] = "idle"
                
                # Responder Agent
                st.session_state.agents["responder"]["status"] = "processing"
                st.session_state.agents["responder"]["calls"] += 1
                time.sleep(0.4)
                final = f"Response for: '{query}'"
                st.session_state.log.append({
                    "agent": "Responder Agent",
                    "input": result,
                    "output": final,
                    "latency": 0.4,
                    "status": "✅"
                })
                st.session_state.agents["responder"]["status"] = "idle"
                
                st.success(final)
            else:
                st.error("Query validation failed")

# Display execution log
if st.session_state.log:
    st.markdown("---")
    st.subheader("📋 Execution Trace")
    for entry in st.session_state.log:
        with st.expander(f"{entry['status']} {entry['agent']} ({entry['latency']}s)"):
            st.write(f"**Input:** {entry['input']}")
            st.write(f"**Output:** {entry['output']}")
            st.write(f"**Latency:** {entry['latency']}s")

# Display metrics
st.markdown("---")
st.subheader("📊 Agent Metrics")
cols = st.columns(4)
for i, (name, data) in enumerate(st.session_state.agents.items()):
    with cols[i]:
        st.metric(
            label=name.capitalize(),
            value=data["calls"],
            delta=f"{data['latency']}s avg"
        )

st.markdown("---")
st.markdown("Built by [Anand](https://github.com/feelgood4everai) • 26 years delivering production systems")
