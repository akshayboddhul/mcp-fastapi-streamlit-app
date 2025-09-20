Inventory Management System
A local data-driven application demonstrating the powerful synergy between a user-friendly Streamlit frontend, a robust FastAPI backend, and an AI agent enabled by a local Model Context Protocol (MCP) server.

This project showcases how to build a full-stack Python application that can be interacted with by both a human user via a web UI and an AI agent via natural language commands.

Key Technologies
FastAPI: A modern, fast (high-performance) web framework for building the backend API.

Streamlit: An open-source app framework for creating interactive web apps in pure Python, serving as the user-friendly frontend.

SQLite: A lightweight, file-based database used to store the inventory data.

MCP (Model Context Protocol): An open standard that allows an AI agent to securely interact with the local application's tools and data.

Architecture
The system is composed of three interconnected components, all running on your local machine.

The Streamlit Frontend communicates with the FastAPI Backend using standard HTTP requests to display and manage inventory data.

The FastAPI Backend handles all data logic and persists the information to an SQLite database file (inventory.db).

A dedicated Local MCP Server exposes the FastAPI endpoints as callable tools. This allows an AI Agent (e.g., GitHub Copilot Chat) to call these tools via natural language commands, effectively bypassing the UI to interact directly with the backend.

Getting Started
Follow these steps to set up and run the application.

Prerequisites
Python 3.8+ installed with pip and venv enabled.

Visual Studio Code installed.

GitHub Copilot Chat Extension and MCP Extension installed in VS Code.

Step 1: Project Setup
Open a terminal or command prompt and create a new project directory.

mkdir InventoryApp
cd InventoryApp

Create and activate a Python virtual environment.

python -m venv venv
.\venv\Scripts\activate

Install all the required Python libraries.

pip install fastapi "uvicorn[standard]" streamlit "mcp[cli]" pandas

Step 2: Create the Application Files
Create the following three files in your InventoryApp directory.

database.py

api.py

app.py

mcp_server.py

Copy the code for each file from the previous conversation.

Step 3: Configure the MCP Server
Open the project in VS Code (File > Open Folder...).

Create a new folder named .vscode in your project's root directory.

Inside the .vscode folder, create a new file named settings.json.

Add the following JSON configuration to the settings.json file. This tells the VS Code MCP extension how to run your local server.

{
    "mcpServers": {
        "Inventory Manager": {
            "command": "python",
            "args": ["${workspaceFolder}\\mcp_server.py"],
            "description": "An MCP server for managing inventory data."
        }
    }
}

Step 4: Run the Application
You will need to run two separate commands in two different terminals.

Run the FastAPI Backend: Open your first terminal, navigate to the project directory, activate your virtual environment, and start the FastAPI server.

uvicorn api:app --reload

Run the Streamlit Frontend: Open a second terminal, activate the virtual environment, and start the Streamlit app. This will open the web UI in your browser.

streamlit run app.py

Your application is now running locally!

How to Use
Method 1: Via the Streamlit Web UI
Open your browser to http://localhost:8501. Here you can use the form to add new items and click the "Refresh Inventory" button to view the database contents.

Method 2: Via an AI Agent
Open the GitHub Copilot Chat in VS Code and try these prompts. The AI will automatically use the Inventory Manager MCP server to interact with the backend.

Prompt: "List all items currently in the inventory."

Prompt: "Add a new item called 'Hammer', with a quantity of 10 and a price of 15.75."

Prompt: "What is the total quantity of 'Hammer' in the database?" (This requires the AI to call a tool, parse the result, and perform a calculation, showcasing the true power of this architecture.)