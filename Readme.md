
# 🧠 LLM-Powered Terminal Assistant using A2A & MCP

### [youtube link](https://youtu.be/nSjj1ZaNP2c) : Deep dive and step by step tutorial of A2A and MCP, including code walthrough

This is an LLM-powered application that allows users to execute terminal commands using simple English queries like:

> "Delete `readme.txt` on my desktop."

It leverages the **A2A** (Agent-to-Agent) and **MCP** (Model Context Protocol) to interpret and execute commands on a Linux system.

---

## 🛠️ Getting Started

Follow these steps to get the system up and running.

### 1. Clone the Repository

```bash
git clone https://github.com/ishanExtreme/a2a_mcp-example.git
cd a2a_mcp-example
```

### 2. Set OpenAI API Key

Export your OpenAI API key to your environment:

```bash
export OPENAI_API_KEY="<your-openai-api-key>"
```

### 3. Create and Activate Virtual Environment

```bash
python -m venv venv or conda create ...
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 4. Install Requirements

```bash
pip install -r requirements.txt
```

---

## 🧩 Running the Application

Ensure all the services are running in separate terminal tabs/windows:

### 🖥️ Start the UI Server

```bash
cd ./client/demo/ui
uv run main.py
```

### 🔁 Start the A2A Server

```bash
cd ./a2a_server
python main.py
```

### 🖥️ Start the MCP Server

```bash
cd ./mcp_server
python mcp_server.py
```

---

## 🌐 Accessing the Application

1. Open your browser and go to: [http://localhost:12000](http://localhost:12000)
2. Navigate to the **Agents** section.
3. Add a **Linux agent** using the following endpoint:

```
http://localhost:10000
```

You are now ready to start chatting and executing Linux commands via natural language!


---

## 🧪 Example Queries

- "Delete the `notes.txt` file on Desktop"
- "List all files in the Documents folder"
- "Create a new directory called `projects`"

---

## 🧠 Built With

- [OpenAI GPT](https://platform.openai.com/)
- A2A Protocol
- MCP Protocol
- FastAPI + Uvicorn
- Python 3.12+

---

## 📜 License

MIT License © 2025

---
