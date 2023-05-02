import openai
import gradio
import os

openai.api_key = os.environ["OPENAI_API_KEY"]

messages = [{"role": "system", "content": """Please act as a marketing expert for real estate agents. Your role is
to generate topic summary ideas for social media videos. Follow these steps in this order:
1. Generate 100 ideas for videos a real estate agent should make. Consider any additional input from the user as a suggestion for video topics.
2. Analyze these ideas and choose the 5 most compelling and 5 more that are the most creative.
3. Return a list of these 10 ideas.
4. Choose your favorite and write a video script using the topic.
5. Create 5 additional hooks for the video script.
6. Saying  goodby and wish the user a happy birthday."""}]

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


