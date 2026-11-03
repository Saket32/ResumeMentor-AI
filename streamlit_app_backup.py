
import streamlit as st
import requests
import json
import uuid

from database import (
    create_database,
    create_session,
    get_sessions,
    get_messages,
    save_message,
    delete_session,
    rename_session
)

# ---------------- CONFIGURATION ----------------

st.set_page_config(
    page_title="SmartChat AI",
    page_icon="🤖",
    layout="wide"
)

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2:1b"

create_database()

# ---------------- AI PERSONALITIES ----------------

prompts = {
    "Friendly Assistant": "You are a helpful and friendly assistant.",
    "Python Tutor": "You are an expert Python tutor. Explain concepts simply with examples.",
    "AI/ML Mentor": "You are an experienced AI/ML engineer. Teach AI and ML with practical examples."
}

# ---------------- SESSION STATE ----------------

if "session_id" not in st.session_state:
    st.session_state.session_id = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- SIDEBAR ----------------

st.sidebar.title("🤖 SmartChat AI")

if st.sidebar.button("➕ New Chat", use_container_width=True):

    new_id = str(uuid.uuid4())

    create_session(new_id)

    st.session_state.session_id = new_id
    st.session_state.messages = []

    st.rerun()

st.sidebar.divider()


st.sidebar.subheader("💬 Your Conversations")

sessions = get_sessions()

for session_id, title in sessions:

    with st.sidebar.expander(f"💬 {title}"):

        if st.button(
            "Open Chat",
            key=f"open_{session_id}",
            use_container_width=True
        ):
            st.session_state.session_id = session_id
            st.session_state.messages = get_messages(session_id)
            st.rerun()

        new_title = st.text_input(
            "Chat title",
            value=title,
            key=f"title_{session_id}"
        )

        if st.button(
            "Save Title",
            key=f"rename_{session_id}"
        ):
            if new_title.strip():
                rename_session(session_id, new_title.strip())
                st.success("Chat renamed!")
                st.rerun()
            else:
                st.warning("Title cannot be empty.")

        if st.button(
            "Delete Chat",
            key=f"delete_{session_id}"
        ):
            delete_session(session_id)

            if st.session_state.session_id == session_id:
                st.session_state.session_id = None
                st.session_state.messages = []

            st.rerun()

st.sidebar.divider()

personality = st.sidebar.selectbox(
    "Choose AI personality",
    list(prompts.keys())
)

system_prompt = prompts[personality]

st.sidebar.caption(f"Active model: {MODEL}")

# ---------------- MAIN SCREEN ----------------

st.title("🤖 SmartChat AI")
st.caption("Your personal AI assistant powered by Llama 3.2")

if st.session_state.session_id is None:

    st.markdown(
        "<h3 style='text-align:center; margin-top:100px;'>"
        "What can I help you with today?"
        "</h3>",
        unsafe_allow_html=True
    )

else:

    # Display selected conversation
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])


# ---------------- OLLAMA STREAMING ----------------

def stream_ollama_response(messages, system_prompt):

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            *messages
        ],
        "stream": True
    }

    with requests.post(
        OLLAMA_URL,
        json=payload,
        stream=True,
        timeout=(10, 300)
    ) as response:

        response.raise_for_status()

        for line in response.iter_lines():

            if line:

                chunk = json.loads(line)

                content = chunk.get("message", {}).get("content", "")

                if content:
                    yield content


# ---------------- CHAT INPUT ----------------

question = st.chat_input("Ask me anything...")

if question:

    # Automatically create a chat if none is selected
    if st.session_state.session_id is None:

        new_id = str(uuid.uuid4())

        create_session(new_id)

        st.session_state.session_id = new_id
        st.session_state.messages = []

    session_id = st.session_state.session_id

    user_message = {
        "role": "user",
        "content": question
    }

    st.session_state.messages.append(user_message)

    save_message(session_id, "user", question)

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        try:

            answer = st.write_stream(
                stream_ollama_response(
                    st.session_state.messages,
                    system_prompt
                )
            )

            assistant_message = {
                "role": "assistant",
                "content": answer
            }

            st.session_state.messages.append(assistant_message)

            save_message(session_id, "assistant", answer)

        except (
            requests.exceptions.RequestException,
            json.JSONDecodeError
        ) as error:

            st.error(f"AI connection error: {error}")

            st.session_state.messages.pop()
