import os
import requests
import uuid
import json
from datetime import datetime
from bs4 import BeautifulSoup
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq client
try:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
except:
    st.error("GROQ_API_KEY not found in environment variables. Please create a .env file with your key.")
    st.stop()

# Initialize session state
if 'sessions' not in st.session_state:
    st.session_state.sessions = {}

if 'current_session' not in st.session_state:
    st.session_state.current_session = None

if 'new_url' not in st.session_state:
    st.session_state.new_url = ""

def fetch_website_content(url):
    """Fetch and extract text content from a website URL"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        text_content = ' '.join([element.get_text().strip() for element in paragraphs])
        
        return text_content if text_content else None
        
    except Exception as e:
        st.error(f"Error fetching website content: {str(e)}")
        return None

def process_content(text, max_length=28000):
    """Clean and truncate text content"""
    cleaned_text = ' '.join(text.split())
    return cleaned_text[:max_length] if len(cleaned_text) > max_length else cleaned_text

def generate_chat_response(user_input, context, history=[]):
    """Generate chatbot response using Groq API with conversation history"""
    try:
        # Build conversation history including context
        messages = [
            {
                "role": "system",
                "content": f"Answer questions using only this context: {context}. do not use the out of webpage informations, just say out of context info. try to use minimum tokens with all nessesory  info."
            }
        ]
        
        # Add conversation history if available
        for exchange in history:
            messages.append({"role": "user", "content": exchange['user']})
            if exchange['bot']:
                messages.append({"role": "assistant", "content": exchange['bot']})
        
        # Add current user input
        messages.append({"role": "user", "content": user_input})
        
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama3-70b-8192",
            temperature=0.4,
            max_tokens=150
        )
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating response: {str(e)}"

def create_session(url, context):
    """Create a new chat session"""
    session_id = str(uuid.uuid4())
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return {
        'id': session_id,
        'url': url,
        'context': context,
        'history': [],
        'created': timestamp,
        'last_accessed': timestamp
    }

def add_to_history(session, user_input, bot_response):
    """Add conversation to session history"""
    session['history'].append({
        'user': user_input,
        'bot': bot_response,
        'timestamp': datetime.now().strftime("%H:%M:%S")
    })
    session['last_accessed'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return session

# Streamlit app layout
st.set_page_config(
    page_title="WebChat Assistant",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar - Session Management
with st.sidebar:
    st.title("💬 Chat Sessions")
    
    # New session form
    with st.form("new_session_form", clear_on_submit=True):
        st.subheader("Start New Chat")
        url = st.text_input("Website URL:", value=st.session_state.new_url, 
                           placeholder="https://example.com")
        submit_new = st.form_submit_button("Start Chat")
        
        if submit_new and url:
            # Validate URL
            if not url.startswith('http'):
                st.error("Please enter a valid URL starting with http:// or https://")
            else:
                with st.spinner("Fetching website content..."):
                    raw_text = fetch_website_content(url)
                    if raw_text:
                        processed_text = process_content(raw_text)
                        new_session = create_session(url, processed_text)
                        session_id = new_session['id']
                        
                        # Save to sessions
                        st.session_state.sessions[session_id] = new_session
                        st.session_state.current_session = session_id
                        st.session_state.new_url = ""
                        st.rerun()
    
    st.divider()
    st.subheader("Your Sessions")
    
    # Display chat sessions
    if not st.session_state.sessions:
        st.info("No chat sessions yet")
    else:
        # Sort sessions by last access time (newest first)
        sorted_sessions = sorted(
            st.session_state.sessions.values(),
            key=lambda x: x['last_accessed'],
            reverse=True
        )
        
        for session in sorted_sessions:
            # Truncate URL for display
            display_url = session['url']
            if len(display_url) > 35:
                display_url = display_url[:15] + "..." + display_url[-15:]
                
            # Display session button
            if st.button(
                f"{display_url}",
                key=f"session_{session['id']}",
                help=f"Created: {session['created']}"
            ):
                st.session_state.current_session = session['id']
                st.rerun()
        
        # Delete session button
        if st.session_state.current_session:
            if st.button("Delete Current Session", use_container_width=True):
                if st.session_state.current_session in st.session_state.sessions:
                    del st.session_state.sessions[st.session_state.current_session]
                    st.session_state.current_session = None
                    st.rerun()

# Main Chat Area
st.title("WebChat Assistant")
st.caption("Chat with any website using AI")

if st.session_state.current_session:
    session = st.session_state.sessions[st.session_state.current_session]
    
    # Display session info
    st.info(f"**Website:** {session['url']}  \n**Started:** {session['created']}")
    
    # Display chat history
    with st.container():
        st.subheader("Chat History")
        
        if not session['history']:
            st.info("No messages yet. Start a conversation below.")
        
        for exchange in session['history']:
            with st.expander(f"You: {exchange['user']}", expanded=True):
                st.write(f"**Assistant:** {exchange['bot']}")
                st.caption(f"Sent at {exchange['timestamp']}")
    
    # User input
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Your message:", key="user_input", 
                                  placeholder="Ask about this website...")
        submit_chat = st.form_submit_button("Send")
        
        if submit_chat and user_input:
            with st.spinner("Thinking..."):
                bot_response = generate_chat_response(
                    user_input, 
                    session['context'], 
                    session['history']
                )
                
                # Update session
                session = add_to_history(session, user_input, bot_response)
                st.session_state.sessions[st.session_state.current_session] = session
                
                # Rerun to update chat display
                st.rerun()
else:
    st.info("👈 Start a new chat session by entering a website URL in the sidebar")
    # st.image("https://images.unsplash.com/photo-1677442135722-5f6d78bcee0d?auto=format&fit=crop&q=80", 
    #          caption="Chat with any website content")
    # st.write("""
    # ### How to use:
    # 1. Enter a website URL in the sidebar
    # 2. Ask questions about the website content
    # 3. Switch between different chat sessions
    # 4. Each session maintains its own conversation history
    # """)
    
# Add footer
st.divider()
st.caption("WebChat Assistant v1.0 | Chat history is stored only in your current browser session")





