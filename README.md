# 🎭 Fun Facts & Jokes Agent 🔢

An interactive conversational CLI agent powered by **LangChain**, **LangGraph**, and **Ollama (llama3.2)** that fetches fresh jokes and fascinating number trivia facts.

---

## 🛠️ Tech Stack & Architecture

- **LLM**: Ollama `llama3.2` with `temperature=0.7` via `langchain-ollama`
- **Framework**: LangGraph `create_react_agent` (prebuilt ReAct reasoning loop with stateful conversation memory)
- **External Free APIs (No Keys Required)**:
  - **JokeAPI** (`https://v2.jokeapi.dev`): High quality jokes across categories (`Any`, `Programming`, `Misc`, `Pun`, `Spooky`, `Christmas`) filtered with `blacklistFlags=nsfw,racist`.
  - **NumbersAPI** (`http://numbersapi.com`): Mathematical and trivia facts about any number or random numbers.

---

## 📁 Project Structure

```
FUN FACTS AGENT/
├── agent.py          # Agent initialization (build_agent), execution (ask), and interactive CLI (main)
├── app.py            # Modern Streamlit web application with chat interface
├── tools.py          # get_joke and get_number_fact @tool definitions
├── requirements.txt  # Python package dependencies
└── README.md         # Documentation & guide
```

---

## 🚀 How to Run

### 1. Prerequisites
- Python 3.10+
- [Ollama](https://ollama.com/) running with `llama3.2`:
  ```bash
  ollama run llama3.2
  ```

### 2. Option A: Web App (Streamlit)
Launch the browser UI on `http://localhost:8501`:
```bash
streamlit run app.py
```

### 3. Option B: CLI Terminal Chat
Run the conversational command-line interface:
```bash
python agent.py
```

---

## 💬 Example Interactions

```
============================================================
   🎭  WELCOME TO THE FUN FACTS & JOKES AGENT!  🔢
============================================================
Ask for jokes (e.g., 'Tell me a programming joke!')
Ask about numbers (e.g., 'What's special about 42?')
Type 'quit', 'exit', or 'q' to leave.
------------------------------------------------------------

Agent ready! Let's have some fun.

You: Tell me a programming joke

Agent:
Here's one for you:

Why do programmers prefer dark mode?
Because light attracts bugs! 🐛

------------------------------------------------------------
You: What's special about the number 42?

Agent:
42 is the number of dots on a pair of standard dice — 21 on each die!
(And of course, according to The Hitchhiker's Guide to the Galaxy, it's the Answer to the Ultimate Question of Life, the Universe, and Everything!)
------------------------------------------------------------
You: exit

Agent: Thanks for chatting! Keep smiling and have a wonderful day! 👋✨
```

---

## ⚙️ Key Design Decisions

| Decision | Reason |
|---|---|
| `temperature=0.7` | High creativity for entertaining delivery and comedic timing |
| Two tools (`get_joke`, `get_number_fact`) | Dedicated tools for jokes and number facts — fits the fun trivia theme |
| `blacklistFlags=nsfw,racist` | Safe content filtering for all audiences |
| Default `category="Any"` | Broadest coverage for jokes when category is unspecified |
| Default `number="random"` | Allows tool invocation without user explicitly specifying a number |
| Fallback Trivia Resilience | Protects user experience if external APIs experience downtime |
| `MemorySaver()` Session Checkpointer | Preserves conversational context across turns within the CLI chat |
