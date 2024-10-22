import google.generativeai as genai

import bot_config

genai.configure(api_key=bot_config.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")
sd = "你是一只的可爱的小猫咪，请用小猫的口吻"


def run(mes):
    response = model.generate_content(sd + mes, safety_settings={
        "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
        "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
        "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
        "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE"
    })
    return response.text
