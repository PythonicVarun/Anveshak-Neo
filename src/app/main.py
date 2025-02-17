import os
import uuid
import logging
import datetime
import streamlit as st
import extra_streamlit_components as stx

from core.llm_response import LLM
from database.db import create_new_chat, delete_chat, get_chat_messages, get_chat_title, get_chats_by_session_id, save_chat_title, save_message

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Streamlit page configuration
st.set_page_config(
    page_title="Anveshak Neo",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
)
mainTitle = st.title("Anveshak Neo 🤖")

def get_manager():
    return stx.CookieManager()

if "cm" not in st.session_state:
    st.session_state.cm = get_manager()

if "session" in st.session_state.cm.cookies:
    session_id = st.session_state.cm.cookies["session"]
else:
    session_id = uuid.uuid4().hex
    st.session_state.cm.set(
        "session",
        session_id,
        expires_at=datetime.datetime.now() + datetime.timedelta(days=365)
    )

# Load the external CSS
css_path = "src/app/stylesheets/styles.css"
if os.path.exists(css_path):
    with open(css_path, "r") as f:
        st.markdown(f"<style>{str(f.read())}</style>", unsafe_allow_html=True)

# Sidebar to display chat sessions with buttons
st.sidebar.title("Anveshak Neo 🤖")

description = st.markdown("""
**Anveshak Neo 🤖** is an AI-powered chatbot that detects emotions from text input. It provides real-time emotional analysis using a trained model, allowing users to engage in meaningful conversations. The chatbot stores past conversations in a PostgreSQL database using SQLAlchemy ORM, enabling users to revisit and continue previous chats. The sidebar displays all existing chat sessions, allowing seamless navigation between different conversations.  

## Creating a New Chat:  
To start a new conversation, simply click the **"Start New Chat"** button in the sidebar. This will create a fresh chat session, separate from previous discussions. Each chat is stored in the database, ensuring that you can return to past conversations anytime.
""")

# Retrieve all chats for the current persistent session
user_chats = get_chats_by_session_id(session_id)

# Initialize session state for selected chat
if "selected_chat_id" not in st.session_state:
    st.session_state.selected_chat_id = None

# Display each chat for the current session in the sidebar
if user_chats:
    count = 1
    for chat in user_chats:
        col1, col2 = st.sidebar.columns([3, 1])
        title = chat.title or f"{chat.created_at.strftime('%d-%m-%Y')}"
        if col1.button(title, key=f"chat-{count}"):
            st.session_state.selected_chat_id = chat.id

        # Display selected chat title in the main area
        if st.session_state.selected_chat_id == chat.id:
            mainTitle.empty()
            description.empty()
            mainTitle = st.title(chat.title or f"**Created At:** {chat.created_at.strftime("%d-%m-%y %I:%M:%S %p")}")

        # Delete chat button functionality
        if col2.button("❌", key=f"delete_{chat.id}"):
            delete_chat(chat.id)
            if st.session_state.selected_chat_id == chat.id:
                st.session_state.selected_chat_id = None
            st.rerun()
        count += 1
else:
    st.sidebar.write("No chats available.")

# Button to start a new chat session
if st.sidebar.button("Start New Chat"):
    st.session_state.selected_chat_id = create_new_chat(session_id)
    st.rerun()

# Initialize session state for chat messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display messages for the selected chat
if st.session_state.selected_chat_id:
    chat_messages = get_chat_messages(st.session_state.selected_chat_id)
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown("**Anveshak Neo:**\n\nHi, I'm Anveshak. How can I help you?")

    for message in chat_messages:
        avatar = "😎" if message.role == "user" else "🤖"
        with st.chat_message(message.role, avatar=avatar):
            role_prefix = "**Mr. GenZ:**\n\n" if message.role == "user" else "**Anveshak Neo:**\n\n"
            st.markdown(role_prefix + message.content)

    # Initialize the AI model with chat history
    model = LLM(chat_messages)
    
    # Input field for user messages
    if prompt := st.chat_input("Message Anveshak"):
        with st.chat_message("user", avatar="😎"):
            st.markdown("**Mr. GenZ:**\n\n" + prompt)

        # Process AI response
        header = full_response = "**Anveshak Neo:**\n\n"
        with st.chat_message("assistant", avatar="🤖"):
            response = st.empty()
            with st.status("Starting Model!", expanded=False) as status:
                st.write("Starting Model!")
                if not get_chat_title(st.session_state.selected_chat_id):
                    title = model.get_title(prompt)
                    save_chat_title(st.session_state.selected_chat_id, title)

                st.write("Extracting emotions from message.")
                status.update(
                    label="Extracting emotions from message.", state="running", expanded=False
                )

                for chunk in model.reply(prompt, chat_id=st.session_state.selected_chat_id, func=save_message):
                    status.update(
                        label="Replying...", state="running", expanded=False
                    )
                    full_response += chunk + " "
                    response.markdown(full_response + "▌")

                response.markdown(full_response)
                st.write("All done!")
                status.update(
                    label="All done!", state="complete", expanded=False
                )

        # Save AI response to the database
        save_message(st.session_state.selected_chat_id, "assistant", full_response.replace(header, ""))
        st.rerun()
else:
    st.write("Please select a chat session from the sidebar or create a new one.")
