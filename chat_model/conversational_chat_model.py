import os

import requests
from dotenv import load_dotenv
from langchain_core.messages import AIMessage
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.system import SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
class ConversationalChatModel :
    ###############################################################################
    # Basic Implementation with a Curl call rather than usinfg some of the inbuilt#
    # features of Lang Chain request Body Parameters :                            #
    # https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference       #
    # /inference#request                                                          #
    ###############################################################################
    def gatewayLLM(self, request_data: str, role: str, system_message: str) :
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
              },
              "systemInstruction": {
                  "role": role,
                  "parts": [
                    {
                      "text": system_message
                    }
                  ]
                },
            }
        url = "https://generativelanguage.googleapis.com/v1beta/models/{0}:generateContent".format(chat_model)
        headers = {
            'Content-Type': 'application/json',
            'X-goog-api-key': api_key
        }
        print(url, payload, headers)
        result = requests.post(url=url, json=payload, headers=headers)
        return result

    def conversation(self, human_message: str):
        chat_model_name = os.getenv("CHAT_MODEL", "Defaulted Model")
        model = ChatGoogleGenerativeAI(model=chat_model_name)

        messages = [
            SystemMessage(content="Solve the following math problem"),
            HumanMessage(content=human_message)
        ]
        result = model.invoke(messages)
        messages.append(AIMessage(content=result.content))
        messages.append(HumanMessage(content="What is this number appproximately equal"
            + "to called in Mathematics?"))
        result = model.invoke(messages)
        return result

if __name__ == "__main__":
    chat_model = ConversationalChatModel()
    result = chat_model.conversation("What is 22 divided by 7?")
    print(f"Result from AI : {result.content}")
