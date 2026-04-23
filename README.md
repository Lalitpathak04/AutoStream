# AutoStream Lead Conversion Agent

An AI-powered system designed to identify user intent and convert social media interactions into qualified business leads using stateful agentic workflows.

---

## 🚀 1. How to Run Locally

### Prerequisites
- Python 3.10+
- A [Groq Cloud](https://console.groq.com/) API Key.

### Setup Instructions
1. **Clone the Repository:**
   ```bash
   git clone <your-repo-url>
   cd <your-repo-name>

2. **Create a Virtual Environment:**
      ```bash
      python -m venv venv
      source venv/bin/activate  # On Windows: venv\Scripts\activate

4. **Install Dependencies:**
      ```bash
      pip install -r requirements.txt

6. **Configure Environment Variables:**
   - Create a .env file in the root directory and add your Groq API key:
      ```Code snippet
      GROQ_API_KEY=gsk_your_key_here

7. **Launch the App:**
      ```bash
      streamlit run frontend.py

## 2. Architecture Explanation

  **Why LangGraph?**

For this project, I chose LangGraph over AutoGen because of its explicit control over state and cyclic logic. While AutoGen is powerful for autonomous, open-ended multi-agent conversations, LangGraph allows for a "Flow Engineering" approach.

In a lead-generation use case, precision is paramount. We cannot afford unpredictable agent behavior or "hallucinated" tool calls. LangGraph’s StateGraph provides a robust framework to enforce a strict logic gate:

Analyze Intent: (Casual vs. Pricing vs. Lead).

Validate Constraints: (Check chat history for Name, Email, and Platform).

Conditional Execution: Only transition to the tools_node once the required schema is satisfied.

How State is Managed
State is managed using a TypedDict named ChatState. It leverages the add_messages reducer, which treats the conversation history as an append-only list of message objects (HumanMessage, AIMessage, ToolMessage).

This architecture allows the agent to maintain "short-term memory" across multiple turns. Instead of manually parsing a giant string of text, the state is passed between nodes. Conditional Edges inspect the last_message of the state to check for tool_calls. If the LLM generates a tool call, the graph routes the state to the ToolNode; otherwise, it returns the response to the user and ends the turn.
















     
