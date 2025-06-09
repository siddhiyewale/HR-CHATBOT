import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Helps to load the API Key
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"         # chat completion url
MODEL_NAME = "mistralai/mistral-7b-instruct"                        # model used(mistral 7B instruct by openrouter)

# Streamlit page setup
st.set_page_config(page_title="Your HR Chatbot", page_icon="🤖")
st.title("🤖 Your HR Chatbot")                                           #Title of the web page
st.write("Ask me anything about HR policies, leave, holidays, or career growth.")

# Function to call LLM
def get_hr_answer(user_input):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [                        #Message to the AI chatbot
            {
                "role": "system",
                "content": "You are a friendly HR assistant who answers clearly and politely. Answer employee questions based on typical HR policies like paid leaves, holidays, work-from-home, recruitment, etc."
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)        # Sending the packages
        response.raise_for_status()  # Raise an exception for HTTP errors

        data = response.json()          # To read the reply
        if "choices" in data:
            return data["choices"][0]["message"]["content"]
        else:                                                             # If something goes wrong
            return "⚠️ API responded but no choices were found. Please try again."
    except Exception as e:
        return f"❌ Error: {str(e)}"

# User Input Questions
user_input = st.text_area("👤 Your question:")

# Button to Get the Reply
if st.button("Get answer"):
    if user_input:
        with st.spinner("Fetching response from HR database..."):       # Loading
            answer = get_hr_answer(user_input)
            st.success(answer)                                      # Getting the answer
    else:
        st.warning("Please enter a question.")                    
