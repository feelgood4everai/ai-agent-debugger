"""
AI Agent Debugger
Visual debugging tool for multi-agent AI systems
"""

import gradio as gr
import json
import time
from datetime import datetime

# Mock agent system for demo purposes
class AgentDebugger:
    def __init__(self):
        self.agents = {
            "intake": {"status": "idle", "calls": 0, "avg_latency": 0.3},
            "validator": {"status": "idle", "calls": 0, "avg_latency": 0.5},
            "processor": {"status": "idle", "calls": 0, "avg_latency": 0.8},
            "responder": {"status": "idle", "calls": 0, "avg_latency": 0.4}
        }
        self.execution_log = []
    
    def run_trace(self, query):
        """Simulate a multi-agent execution with tracing."""
        self.execution_log = []
        results = []
        
        # Agent 1: Intake
        start = time.time()
        self.agents["intake"]["status"] = "processing"
        self.agents["intake"]["calls"] += 1
        time.sleep(0.2)
        self.execution_log.append({
            "agent": "Intake Agent",
            "input": query,
            "output": f"Parsed query: '{query}'",
            "latency": round(time.time() - start, 3),
            "tokens": 150,
            "status": "success"
        })
        self.agents["intake"]["status"] = "idle"
        
        # Agent 2: Validator
        start = time.time()
        self.agents["validator"]["status"] = "processing"
        self.agents["validator"]["calls"] += 1
        time.sleep(0.3)
        is_valid = len(query) > 5
        self.execution_log.append({
            "agent": "Validator Agent",
            "input": f"Parsed query: '{query}'",
            "output": f"Valid: {is_valid}",
            "latency": round(time.time() - start, 3),
            "tokens": 200,
            "status": "success" if is_valid else "error"
        })
        self.agents["validator"]["status"] = "idle"
        
        if not is_valid:
            return "Error: Query too short", self.format_log(), self.format_metrics()
        
        # Agent 3: Processor
        start = time.time()
        self.agents["processor"]["status"] = "processing"
        self.agents["processor"]["calls"] += 1
        time.sleep(0.4)
        result = f"Processed: '{query}' -> Action identified"
        self.execution_log.append({
            "agent": "Processor Agent",
            "input": f"Valid: {is_valid}",
            "output": result,
            "latency": round(time.time() - start, 3),
            "tokens": 350,
            "status": "success"
        })
        self.agents["processor"]["status"] = "idle"
        
        # Agent 4: Responder
        start = time.time()
        self.agents["responder"]["status"] = "processing"
        self.agents["responder"]["calls"] += 1
        time.sleep(0.2)
        final = f"Final response for: '{query}'"
        self.execution_log.append({
            "agent": "Responder Agent",
            "input": result,
            "output": final,
            "latency": round(time.time() - start, 3),
            "tokens": 180,
            "status": "success"
        })
        self.agents["responder"]["status"] = "idle"
        
        return final, self.format_log(), self.format_metrics()
    
    def format_log(self):
        """Format execution log as markdown."""
        lines = ["## Execution Trace\n"]
        for i, entry in enumerate(self.execution_log, 1):
            status_emoji = "✅" if entry["status"] == "success" else "❌"
            lines.append(f"### Step {i}: {entry['agent']} {status_emoji}")
            lines.append(f"- **Input:** {entry['input']}")
            lines.append(f"- **Output:** {entry['output']}")
            lines.append(f"- **Latency:** {entry['latency']}s")
            lines.append(f"- **Tokens:** {entry['tokens']}")
            lines.append("")
        return "\n".join(lines)
    
    def format_metrics(self):
        """Format metrics as markdown table."""
        lines = ["## Agent Metrics\n"]
        lines.append("| Agent | Calls | Avg Latency | Status |")
        lines.append("|-------|-------|-------------|--------|")
        for name, data in self.agents.items():
            status_emoji = "🟢" if data["status"] == "idle" else "🟡"
            lines.append(f"| {name.capitalize()} | {data['calls']} | {data['avg_latency']}s | {status_emoji} {data['status']} |")
        return "\n".join(lines)

# Initialize debugger
debugger = AgentDebugger()

# Gradio interface
def trace_agents(query):
    if not query.strip():
        return "Please enter a query", "No execution yet", debugger.format_metrics()
    result, log, metrics = debugger.run_trace(query)
    return result, log, metrics

with gr.Blocks(title="AI Agent Debugger") as demo:
    gr.Markdown("# 🤖 AI Agent Debugger")
    gr.Markdown("Visual debugging tool for multi-agent AI systems. Enter a query to see step-by-step execution.")
    
    with gr.Row():
        with gr.Column(scale=1):
            query_input = gr.Textbox(
                label="Enter your query",
                placeholder="e.g., 'Process order #12345' or 'Check inventory for widget ABC'",
                lines=2
            )
            submit_btn = gr.Button("🔍 Trace Execution", variant="primary")
            
            gr.Markdown("### Example Queries:")
            gr.Markdown("- `Process refund for order #456`")
            gr.Markdown("- `Check status of ticket #789`")
            gr.Markdown("- `Update customer address`")
        
        with gr.Column(scale=2):
            final_output = gr.Textbox(label="Final Output", lines=2)
    
    with gr.Row():
        with gr.Column():
            execution_log = gr.Markdown(label="Execution Trace")
        with gr.Column():
            metrics_table = gr.Markdown(label="Agent Metrics")
    
    submit_btn.click(
        fn=trace_agents,
        inputs=[query_input],
        outputs=[final_output, execution_log, metrics_table]
    )
    
    gr.Markdown("---")
    gr.Markdown("📊 This is a demo of the AI Agent Debugger. In production, it connects to your actual multi-agent system.")

if __name__ == "__main__":
    demo.launch()
