import os
import google.generativeai as genai
from dotenv import load_dotenv


class GemChat:
    def __init__(self):
        load_dotenv()
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

        self.generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }

        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=self.generation_config,
            # safety_settings = Adjust safety settings
            # See https://ai.google.dev/gemini-api/docs/safety-settings
        )

        self.history = [
            {
                "role": "user",
                "parts": [
                    "You're a health bot, guide users based on the input symptoms and keep your answers concise."],
            },
            {
                "role": "model",
                "parts": [
                    "Understood. I will act as a health doctor bot. And give answers in short.\n",
                ],
            },
        ]
        self.chat_session = self.model.start_chat(history=self.history)

    def sendmsg(self, msg):
        self.history.append({"role": "user", "parts": [msg]})

        response = self.chat_session.send_message(msg)
        self.history.append({"role": "model", "parts": [response.text]})

        return response.text
