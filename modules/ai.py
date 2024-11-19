import google.generativeai as genai

import bot_config

genai.configure(api_key=bot_config.GEMINI_API_KEY)
model = genai.GenerativeModel(bot_config.MODEL)
starting = "你是一只的可爱的小猫咪，请用小猫的口吻对于"
short = "本次输出请尽量简短，字数最好30字以内"


def run(mes):
    response = model.generate_content(starting + mes, safety_settings={
        "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
        "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
        "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
        "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE"
    })
    print(starting + mes)
    return response.text
