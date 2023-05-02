import openai
import gradio
import os

openai.api_key = os.environ["OPENAI_API_KEY"]

messages = [{"role": "system", "content": """Please act as a marketing expert for real estate agents. Your role is
to generate ideas for videos. Consider today's date, and develop 10 ideas for videos that a real estate agent could make today.
Then consider 10 additional outside the box ideas. The second 10 should be creative and make us pause when we read them. Return the 
best 5 from each category and label which category they came from."""}]

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


