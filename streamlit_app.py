# streamlit_app.py
import streamlit as st
import asyncio
from concurrent.futures import ThreadPoolExecutor
from main import poetry_agent, get_session
from connection import get_config
from agents import Runner
from agents.exceptions import InputGuardrailTripwireTriggered

# Page config
st.set_page_config(
    page_title="Poetry AI (Urdu + English)",
    page_icon="🪶",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# App Header
st.title("🪶 AI Poetry Companion")
st.markdown("""
<style>
    body {
        background-color: #f9f9f9;
    }
    .stTextInput textarea {
        border: 2px solid #00b4d8;
        border-radius: 10px;
    }
    .stButton>button {
        background-color: #00b4d8;
        color: white;
        font-weight: bold;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("**Bilingual Poetry Generator (Urdu + English)**")
st.caption("Powered by Agentic AI with input/output guardrails 💡")

# Text input area
user_input = st.text_area(
    "Enter your poetry theme or request:",
    placeholder="e.g. Write a ghazal about rain in Urdu...",
    height=150
)

# Chat memory area (optional)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def run_poetry_prompt(prompt: str) -> str:
    async def run_poetry():
        session = get_session()
        try:
            result = await Runner.run(
                poetry_agent,
                input=prompt,
                run_config=get_config(),
                session=session,
            )
            if not result or not getattr(result, "final_output", None):
                return "The model returned no text. Please try again with a shorter prompt."
            return result.final_output
        except InputGuardrailTripwireTriggered:
            return "Your request was rejected by the guardrail. Try a poem-related prompt like 'write a short Urdu ghazal about rain'."
        except Exception as exc:
            return f"Poetry generation failed: {exc}"

    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(run_poetry())
    else:
        with ThreadPoolExecutor(max_workers=1) as pool:
            return pool.submit(asyncio.run, run_poetry()).result()

# Generate button
if st.button("✨ Generate Poem"):
    if not user_input.strip():
        st.warning("Please enter something first.")
    else:
        with st.spinner("Composing your poem... 🎭"):
            poem_output = run_poetry_prompt(user_input)

        st.session_state.chat_history.append(
            {"user": user_input, "agent": poem_output}
        )

# Display chat history
if st.session_state.chat_history:
    for i, chat in enumerate(st.session_state.chat_history[::-1]):
        with st.expander(f"🧍 You: {chat['user'][:30]}..."):
            st.markdown(f"**🧍 You:** {chat['user']}")
            st.markdown(f"**🤖 Agent:**\n{chat['agent']}")
