import openai
import gradio
import os
from tenacity import retry, wait_fixed, stop_after_attempt

openai.api_key = os.environ["OPENAI_API_KEY"]

initial_messages = [{"role": "system", "content": """Please act as a marketing expert for real estate agents. Your role is
to generate topic summary ideas for social media videos. Follow these steps in this order:
1. Before you execute any steps, consider the last input from the user as a suggestion for the types of topics you should create.
2. Generate 100 ideas for videos a real estate agent should make and choose the 10 most compelling. Do not return all 100 ideas.
3. Return a list of these 10 most compelling ideas."""}]

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

def wrapped_chat_gpt(user_input):
    # Replace the following line with your method to retrieve the messages list for the current user
    messages = initial_messages.copy()

    reply, updated_messages = CustomChatGPT(user_input, messages)

    # Replace the following line with your method to store the updated messages list for the current user
    # Store updated_messages

    return reply

demo = gradio.Interface(fn=wrapped_chat_gpt, inputs="text", outputs="text", title="Video Idea Generator")

demo.launch(inline=False)


