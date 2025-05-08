from Tools.todo import TodoManagerTool
from dotenv import load_dotenv
from smolagents import LiteLLMModel, CodeAgent, Tool
import os

load_dotenv()
# === LiteLLM Model Setup ===
model = LiteLLMModel(
    "gemini/gemini-2.0-flash",
    temperature=0.2,
    api_key=os.getenv("GEMINI_API_KEY"),  # Replace with your actual key or load from env
    max_token=8000
)
# === Code Agent Setup ===
todo_tool = TodoManagerTool()
manager_agent = CodeAgent(
    tools=[todo_tool],
    model=model,
    max_steps=10,
    additional_authorized_imports=[
        'math', 'statistics', 'datetime', 'collections', 'queue', 'random', 're',
        'unicodedata', 'itertools', 'time', 'stat'
    ]
)
