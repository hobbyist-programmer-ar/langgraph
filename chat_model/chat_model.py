import os
import requests
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Dict, Union

load_dotenv()
class ChatModel :
    def gatewayLLM(self, request_data: str) :
        chat_model = os.getenv("CHAT_MODEL", "Defaulted Model")
        api_key = os.getenv("GOOGLE_API_KEY", "Defaulted Key")
        temperature = os.getenv("TEMPERATURE", 0)
        payload ={
              'contents': [
                {
                  'parts': [
                    {
                      'text': request_data
                    }
                  ],
                }
              ],
              'generation_config': {
                  'temperature': temperature,
                  'top_p': 0.2,
                  'top_k': 1
              }
            }
        url = "https://generativelanguage.googleapis.com/v1beta/models/{0}:generateContent".format(chat_model)
        headers = {
            'Content-Type': 'application/json',
            'X-goog-api-key': api_key
        }
        print(url, payload, headers)
        result = requests.post(url=url, json=payload, headers=headers)
        return result

if __name__ == "__main__":
    chat_model = ChatModel()
    result = chat_model.gatewayLLM("What is a Type C Cable?")
    print(result.content)
