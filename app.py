import openai
import os
import streamlit as st
from tenacity import retry, wait_fixed, stop_after_attempt

# Set OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

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
    """
    Call OpenAI's ChatCompletion API with retries for transient errors.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=1000  # Adjust token limit to fit your needs
        )
        return response
    except openai.error.OpenAIError as e:
        raise RuntimeError(f"OpenAI API error: {e}")

def CustomChatGPT(user_input, messages):
    """
    Customize ChatGPT's interaction based on user input and previous messages.
    """
    if user_input.strip():
        messages.append({"role": "user", "content": user_input})
    else:
        messages.append({"role": "user", "content": "Please generate general video ideas for a real estate agent."})
    
    response = call_openai_api(messages)
    ChatGPT_reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": ChatGPT_reply})
    return ChatGPT_reply, messages

# Streamlit app setup
st.title("Video Idea Generator for Real Estate Agents")
st.write("Enter a topic suggestion or leave it blank for general video ideas.")

# User input section
user_input = st.text_input("Enter a topic:", placeholder="E.g., tips for first-time homebuyers")
generate_button = st.button("Generate Ideas")

# Generate ideas on button click
if generate_button:
    messages = initial_messages.copy()
    try:
        with st.spinner("Generating video ideas..."):
            reply, _ = CustomChatGPT(user_input, messages)
        st.subheader("Here are the top video ideas:")
        st.write(reply)
    except RuntimeError as e:
        st.error(f"Error: {e}")
    except Exception as e:
        st.error("An unexpected error occurred. Please try again.")

