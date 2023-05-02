import openai
import gradio
import os

openai.api_key = os.environ["OPENAI_API_KEY"]

messages = [{"role": "system", "content": """Please create engaging and informative video scripts for real 
estate agents to use on social media. The target audience is potential homebuyers and sellers.
The tone should be professional and friendly, with a focus on building trust and showcasing the agent's expertise. 
Please incorporate a strong call-to-action at the end of each script, 
encouraging viewers to contact the agent for more information or assistance. 
Write only the words the agent should read into the camera. Once you create the script, analyze it and determine 5 
engaging hooks that could replace the first sentence. Analyze those 5 hooks, pick the best one, and replace the 
existing hook in the script you wrote with the new one. Deliver the script with the new hook included."""}]

def CustomChatGPT(user_input):
    messages.append({"role": "user", "content": user_input})
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = messages
    )
    ChatGPT_reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": ChatGPT_reply})
    return ChatGPT_reply

demo = gradio.Interface(fn=CustomChatGPT, inputs = "text", outputs = "text", title = "Real Estate Video Script Writer")

demo.launch(inline = False)


