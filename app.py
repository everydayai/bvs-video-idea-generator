import openai
import gradio
import os

openai.api_key = os.environ["OPENAI_API_KEY"]

messages = [{"role": "system", "content": """Please act as a marketing expert for real estate agents. Your role is
to generate topic summary ideas for social media videos. Follow these steps in this order:
1. Before you execute any steps, consider the last input from the user as a suggestion for the types of topics you should create.
2. Generate 100 ideas for videos a real estate agent should make, and analyze them to choose the 10 most compelling. Do not return all 100 ideas.
3. Return a list of these 10 most compelling ideas."""}]

def CustomChatGPT(user_input):
    messages.append({"role": "user", "content": user_input})
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = messages
    )
    ChatGPT_reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": ChatGPT_reply})
    return ChatGPT_reply

demo = gradio.Interface(fn=CustomChatGPT, inputs = "text", outputs = "text", title = "Video Idea Generator")

demo.launch(inline = False)


