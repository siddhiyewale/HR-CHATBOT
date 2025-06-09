import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load API Key
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "mistralai/mistral-7b-instruct"

# Streamlit App UI
st.set_page_config(page_title="HR Chatbot", page_icon="💼")
st.title("💼 HR Chatbot")
st.write("Ask me anything about HR policies, leave, holidays, or recruitment.")

# Function to call LLM
def get_hr_answer(user_input):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You are an HR assistant for a company. Answer employee questions based on typical HR policies like paid leaves, holidays, work-from-home, recruitment, etc."
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors

        data = response.json()
        if "choices" in data:
            return data["choices"][0]["message"]["content"]
        else:
            return "⚠️ API responded but no choices were found. Please try again."
    except Exception as e:
        return f"❌ Error: {str(e)}"

# User Input Field
user_input = st.text_input("👤 Your question:")

# Button to Ask
if st.button("Ask HR"):
    if user_input:
        with st.spinner("Fetching response from HR database..."):
            answer = get_hr_answer(user_input)
            st.success(answer)
    else:
        st.warning("Please enter a question.")
