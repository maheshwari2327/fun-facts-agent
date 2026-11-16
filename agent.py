"""
agent.py - Conversational Fun Facts & Jokes CLI Agent

Stack:
  LLM       : Ollama llama3.2, temperature=0.7 (via langchain-ollama)
  Framework : LangGraph create_react_agent (prebuilt ReAct loop)
  APIs      : JokeAPI (v2.jokeapi.dev) + NumbersAPI (numbersapi.com) — free, no key
"""

import sys
import warnings
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

from tools import get_joke, get_number_fact

# Suppress deprecation notices for a clean CLI output
warnings.filterwarnings("ignore", category=UserWarning)

SYSTEM_PROMPT = (
    "You are a fun and entertaining trivia companion! You have two tools: get_joke "
    "to fetch a fresh joke, and get_number_fact to find fascinating facts about numbers. "
    "Use them to delight, surprise, and amuse the user. If someone asks for a joke, fetch "
    "one and deliver it with good timing. If they ask about a number, share the fact "
    "enthusiastically. Keep the energy light, funny, and engaging!"
)


def build_agent(use_memory: bool = True):
    """
    Build and return the ReAct agent using Ollama llama3.2 and LangGraph.
    """
    llm = ChatOllama(model="llama3.2", temperature=0.7)
    tools = [get_joke, get_number_fact]
    checkpointer = MemorySaver() if use_memory else None

    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=SYSTEM_PROMPT,
        checkpointer=checkpointer,
    )
    return agent


def ask(agent, query: str, config: dict | None = None) -> str:
    """
    Send a query to the agent and return its response string.
    """
    if config is None and getattr(agent, "checkpointer", None) is not None:
        config = {"configurable": {"thread_id": "fun-facts-session"}}

    inputs = {"messages": [("user", query)]}
    if config:
        result = agent.invoke(inputs, config=config)
    else:
        result = agent.invoke(inputs)

    messages = result.get("messages", [])
    if messages:
        last_message = messages[-1]
        content = getattr(last_message, "content", "")
        if isinstance(content, list):
            parts = []
            for item in content:
                if isinstance(item, str):
                    parts.append(item)
                elif isinstance(item, dict) and "text" in item:
                    parts.append(item["text"])
            return "\n".join(parts)
        return str(content)
    return "No response received."


def main():
    """
    Interactive while-loop CLI chat. Exit on 'quit', 'exit', 'q', or Ctrl+C.
    """
    print("=" * 60)
    print("   🎭  WELCOME TO THE FUN FACTS & JOKES AGENT!  🔢")
    print("=" * 60)
    print("Ask for jokes (e.g., 'Tell me a programming joke!')")
    print("Ask about numbers (e.g., 'What's special about 42?')")
    print("Type 'quit', 'exit', or 'q' to leave.")
    print("-" * 60)

    print("\nConnecting to Ollama llama3.2...")
    try:
        agent = build_agent()
        print("Agent ready! Let's have some fun.\n")
    except Exception as e:
        print(f"\n[Error] Failed to initialize agent: {e}")
        print("Please ensure Ollama is installed and running with 'ollama run llama3.2'.")
        return

    session_config = {"configurable": {"thread_id": "cli-user-session"}}

    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue

            if user_input.lower() in ("quit", "exit", "q"):
                print("\nAgent: Thanks for chatting! Keep smiling and have a wonderful day! 👋✨")
                break

            print("\nAgent:")
            response = ask(agent, user_input, config=session_config)
            print(f"{response}\n")
            print("-" * 60)

        except (KeyboardInterrupt, EOFError):
            print("\n\nAgent: Session interrupted. Catch you later! 👋✨")
            break
        except Exception as e:
            print(f"\n[Error]: {e}\n")


if __name__ == "__main__":
    main()
