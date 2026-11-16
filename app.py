import uuid
import streamlit as st
from agent import build_agent, ask

# Page configuration
st.set_page_config(
    page_title="Fun Facts & Jokes Agent",
    page_icon="🎭",
    layout="centered",
)

# Custom header styling
st.title("🎭 Fun Facts & Jokes Agent 🔢")
st.caption("Powered by LangGraph ReAct Agent, Ollama llama3.2, JokeAPI & NumbersAPI")


# Cache the agent instance so it doesn't re-initialize on every rerun
@st.cache_resource
def get_agent():
    return build_agent()


try:
    agent = get_agent()
except Exception as e:
    st.error(f"⚠️ Could not connect to Ollama: {e}")
    st.info("Make sure Ollama is running locally with `ollama run llama3.2`.")
    st.stop()

# Initialize session state for conversation history and unique thread ID
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hello there! 😄 I'm your trivia companion. Ask me for a joke "
                "(e.g., Programming, Pun, Spooky) or any fascinating fact about numbers!"
            ),
        }
    ]

# Sidebar with quick sample prompts and clear action
with st.sidebar:
    st.header("⚡ Quick Sparks")
    quick_prompts = [
        "Tell me a programming joke! 💻",
        "What's special about the number 42? 🎲",
        "Give me a pun joke! 🥖",
        "Surprise me with a random number fact! 🔢",
        "Tell me a spooky joke! 👻",
    ]

    selected_prompt = None
    for qp in quick_prompts:
        if st.button(qp, use_container_width=True):
            selected_prompt = qp

    st.divider()
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Chat reset! What fun trivia or joke can I share next?",
            }
        ]
        st.session_state.session_id = str(uuid.uuid4())
        st.rerun()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input handling (via chat input or sidebar quick prompt)
user_query = st.chat_input("Ask for a joke or a number fact...") or selected_prompt

if user_query:
    # 1. Append & display user message
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    # 2. Invoke the agent
    with st.chat_message("assistant"):
        with st.spinner("Brewing up some laughs and trivia..."):
            try:
                config = {
                    "configurable": {"thread_id": st.session_state.session_id}
                }
                response = ask(agent, user_query, config=config)
                st.markdown(response)
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )
            except Exception as e:
                error_msg = f"Oops! An error occurred: {e}"
                st.error(error_msg)
                st.session_state.messages.append(
                    {"role": "assistant", "content": error_msg}
                )
