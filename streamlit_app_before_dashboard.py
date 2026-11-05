
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
    rename_session,
    get_available_documents
)

from document_manager import (
    process_pdf,
    search_documents,
    create_document_context
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

if "processed_uploads" not in st.session_state:
    st.session_state.processed_uploads = set()


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

        if st.button("Save Title", key=f"rename_{session_id}"):

            if new_title.strip():
                rename_session(session_id, new_title.strip())
                st.success("Chat renamed!")
                st.rerun()
            else:
                st.warning("Title cannot be empty.")

        if st.button("Delete Chat", key=f"delete_{session_id}"):

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

    st.info("Start a new chat to upload and discuss your PDF documents.")

else:

    session_id = st.session_state.session_id

    # Display previous messages
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])


    # ---------------- PDF UPLOAD ----------------

    st.divider()
    st.subheader("📄 Chat with your documents")

    access_type = st.radio(
        "Document access",
        ["private", "shared"],
        horizontal=True,
        format_func=lambda x: (
            "Private — only this chat"
            if x == "private"
            else "Shared — available in all chats"
        ),
        key=f"access_{session_id}"
    )

    uploaded_files = st.file_uploader(
        "Upload PDF documents",
        type=["pdf"],
        accept_multiple_files=True,
        key=f"uploader_{session_id}"
    )

    if uploaded_files:

        for uploaded_file in uploaded_files:

            # Unique key for this upload in the current Streamlit session
            upload_key = (
                session_id,
                uploaded_file.name,
                uploaded_file.size
            )

            if upload_key not in st.session_state.processed_uploads:

                with st.spinner(f"Processing {uploaded_file.name}..."):

                    try:

                        result = process_pdf(
                            pdf_file=uploaded_file,
                            session_id=session_id,
                            access_type=access_type
                        )

                        st.session_state.processed_uploads.add(upload_key)

                        st.success(
                            f"Uploaded {result['filename']} "
                            f"({result['chunks']} chunks)"
                        )

                    except Exception as error:
                        st.error(
                            f"Could not process {uploaded_file.name}: {error}"
                        )


    # ---------------- AVAILABLE DOCUMENTS ----------------

    documents = get_available_documents(session_id)

    with st.expander("📚 Available documents", expanded=False):

        if documents:

            for document_id, filename, doc_access in documents:

                access_label = (
                    "Private"
                    if doc_access == "private"
                    else "Shared"
                )

                st.write(f"📄 **{filename}** — {access_label}")

        else:
            st.caption("No documents uploaded yet.")


# ---------------- OLLAMA STREAMING ----------------

def stream_ollama_response(messages, system_prompt):

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
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

                content = chunk.get(
                    "message", {}
                ).get("content", "")

                if content:
                    yield content


# ---------------- CHAT INPUT ----------------

question = st.chat_input("Ask me anything...")

if question:

    # Create a chat automatically if none exists
    if st.session_state.session_id is None:

        new_id = str(uuid.uuid4())

        create_session(new_id)

        st.session_state.session_id = new_id
        st.session_state.messages = []

        st.rerun()

    session_id = st.session_state.session_id

    # Save and display user message
    user_message = {
        "role": "user",
        "content": question
    }

    st.session_state.messages.append(user_message)

    save_message(session_id, "user", question)

    with st.chat_message("user"):
        st.markdown(question)


    # ---------------- DOCUMENT RETRIEVAL ----------------

    context = ""

    try:

        retrieved_chunks = search_documents(
            question=question,
            session_id=session_id,
            n_results=5
        )

        context = create_document_context(retrieved_chunks)

    except Exception as error:

        st.warning(f"Document search issue: {error}")


    # ---------------- GENERATE AI RESPONSE ----------------

    if context:

        final_system_prompt = (
            system_prompt
            + "\n\n"
            + "The user may ask questions about uploaded documents. "
            + "When document context is supplied, answer document-related "
            + "questions using only that context. Do not invent facts. "
            + "If the answer is not present in the context, say so."
        )

        messages_for_ai = [
            *st.session_state.messages[:-1],
            {
                "role": "user",
                "content": (
                    f"Document context:\n{context}\n\n"
                    f"Question: {question}"
                )
            }
        ]

    else:

        final_system_prompt = system_prompt

        messages_for_ai = st.session_state.messages


    with st.chat_message("assistant"):

        try:

            answer = st.write_stream(
                stream_ollama_response(
                    messages_for_ai,
                    final_system_prompt
                )
            )

            assistant_message = {
                "role": "assistant",
                "content": answer
            }

            st.session_state.messages.append(assistant_message)

            save_message(
                session_id,
                "assistant",
                answer
            )

        except (
            requests.exceptions.RequestException,
            json.JSONDecodeError
        ) as error:

            st.error(f"AI connection error: {error}")

            st.session_state.messages.pop()
