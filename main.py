import os
import re
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with Gemini-Pro!",
    page_icon=":brain:",  # Favicon emoji
    layout="centered",  # Page layout option
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')


# create a function for extracting the user message
def extract_words_after_prompt(text):
    pattern = r'(?<=prompt:)\s*(.*)'
    matches = re.findall(pattern, text)
    words_str = ' '.join(matches)
    return words_str


# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role


# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Display the chatbot's title on the page
st.title("🤖 HUNTAH PRO - ChatBot")

# Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        output = message.parts[0].text
        if 'prompt:' in output:
            output = extract_words_after_prompt(text=output)
        st.markdown(output)

# Input field for user's message
user_prompt = st.chat_input(placeholder="Ask Huntah-Pro...")
if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)

    # Send user's message to Gemini-Pro and get the response
    gemini_response = st.session_state.chat_session.send_message(
        f'''context: you are an expert statistician with vast knowledge of data science 
        and analytics and statistics. You do not know anything about any other thing outside stats and
        data science. You have two jobs, answer data science and analytics questions and respond to greetings
        when you are being greeted.
        prompt: {user_prompt}''')

    # Display Gemini-Pro's response
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)
