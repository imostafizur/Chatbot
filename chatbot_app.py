import streamlit as st
import requests
import time
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []

if "api_key" not in st.session_state:
    st.session_state.api_key = os.environ.get("OPENROUTER_API_KEY", "")

# Function to get response from OpenRouter
def get_chatbot_response(user_input):
    """
    Get a response from OpenRouter API.
    
    Args:
        user_input (str): The user's message
        
    Returns:
        str: The chatbot's response
    """
    api_key = st.session_state.api_key
    
    if not api_key:
        return "⚠️ API key not configured. Please enter your OpenRouter API key in the sidebar."
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://localhost:8501",  # Update in production
    }
    
    # Prepare conversation history
    conversation = [{"role": msg["role"], "content": msg["content"]} 
                   for msg in st.session_state.messages]
    
    # Add the new user message
    conversation.append({"role": "user", "content": user_input})
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json={
                "model": "openai/gpt-3.5-turbo",  # You can change this to other models
                "messages": conversation,
                "max_tokens": 500,
                "temperature": 0.7,
            },
            timeout=30,  # Timeout after 30 seconds
        )
        
        response.raise_for_status()  # Raise exception for HTTP errors
        response_data = response.json()
        
        # Extract the assistant's message
        if "choices" in response_data and len(response_data["choices"]) > 0:
            return response_data["choices"][0]["message"]["content"]
        else:
            return "Sorry, I couldn't generate a response. Please try again."
    
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return f"I encountered an error while processing your request: {str(e)}"

# Sidebar for settings
with st.sidebar:
    st.header("API Configuration")
    
    # API Key input
    api_key_input = st.text_input(
        "OpenRouter API Key", 
        value=st.session_state.api_key,
        type="password",
        help="Enter your OpenRouter API key here"
    )
    
    # Update API key in session state when changed
    if api_key_input != st.session_state.api_key:
        st.session_state.api_key = api_key_input
    
    st.divider()
    
    # Model selection
    model = st.selectbox(
        "Select Model",
        ["openai/gpt-3.5-turbo", "openai/gpt-4", "anthropic/claude-3-opus", "anthropic/claude-3-sonnet"],
        index=0
    )
    
    # Temperature setting
    temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
    
    # Clear chat button
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Application title
st.title("🤖 AI Chatbot")
st.markdown("""
This chatbot uses OpenRouter to provide intelligent responses. Type your message below to get started!
""")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "timestamp" in message:
            st.caption(f"{message['timestamp']}")

# User input
user_input = st.chat_input("Ask me anything...")

# Process user input
if user_input:
    # Add user message to chat history
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.messages.append({"role": "user", "content": user_input, "timestamp": timestamp})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
        st.caption(timestamp)
    
    # Show the bot "thinking" and generate response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.spinner("Thinking..."):
            bot_response = get_chatbot_response(user_input)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Display the response
            message_placeholder.markdown(bot_response)
            st.caption(timestamp)
    
    # Add bot response to chat history
    st.session_state.messages.append({"role": "assistant", "content": bot_response, "timestamp": timestamp})