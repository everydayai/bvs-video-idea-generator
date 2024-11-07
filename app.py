import openai
import os
import streamlit as st
from tenacity import retry, wait_fixed, stop_after_attempt

# Set OpenAI API key from environment variables
openai.api_key = os.environ["OPENAI_API_KEY"]

# Define the initial system message
initial_messages = [{"role": "system", "content": """Please act as a marketing expert for real estate agents. Your role is
to generate topic summary ideas for social media videos. Follow these steps in this order:
1. Before you execute any steps, consider the last input from the user as a suggestion for the types of topics you should create if
they submit one. If they don't submit a topic idea then assume they would like ideas for marketing videos for a real estate agent.
2. Generate 100 total ideas for videos a real estate agent should make. Some should be ideas 
for simple marketing videos, creative social media content, educational videos, and a few that are outside the box.
Reply with the 10 overall best ideas. Include a short, up to 2 sentence long description of each idea. Do not return all 100 ideas."""}]

@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
def call_openai_api(messages):
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

def CustomChatGPT(user_input, messages):
    messages.append({"role": "user", "content": user_input})
    response = call_openai_api(messages)
    ChatGPT_reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": ChatGPT_reply})
    return ChatGPT_reply, messages

# Streamlit app setup
st.title("Video Idea Generator for Real Estate Agents")
st.write("Enter a topic suggestion or leave it blank for general video ideas.")

user_input = st.text_input("Enter a topic:")
generate_button = st.button("Generate Ideas")

if generate_button:
    messages = initial_messages.copy()
    reply, _ = CustomChatGPT(user_input, messages)
    st.write("Here are the top video ideas:")
    st.write(reply)
