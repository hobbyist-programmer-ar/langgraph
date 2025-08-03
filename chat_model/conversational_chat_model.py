import logging
import os
from typing import List

import requests
from dotenv import load_dotenv
from langchain_core.messages import AIMessage
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.system import SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from chat_model.message_type import MessageType
from chat_model.persistance.save_chat import ChatMessagePersistance

load_dotenv()
logging.basicConfig(level=os.getenv("LOGGING_LEVEL", logging.INFO))
chat_history = []


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

    def conversational_chatbot(self, messages: List) :
        chat_model_name = os.getenv("CHAT_MODEL", "Defaulted Model")
        model = ChatGoogleGenerativeAI(model=chat_model_name)
        result = model.invoke(messages)
        return result

    def set_context(self, message: str):
        persistence = ChatMessagePersistance()
        context = SystemMessage(content=message)
        chat_history.append(context)
        persistence.save_message(message, MessageType.SYSTEM_MESSAGE)
        logging.info("System Context Set Successfully")

    def start_coversation(self):
        persistence = ChatMessagePersistance()
        system_message = input("Enter the System Context : ")
        self.set_context(system_message)
        while True :
            query = input("You : ")
            if query.lower() == "exit":
                break
            chat_history.append(HumanMessage(content=query))
            persistence.save_message(query, MessageType.USER_MESSAGE)
            result = self.conversational_chatbot(chat_history)
            response = result.content
            print(f"AI Response : {response}")
            chat_history.append(AIMessage(content=response))
            persistence.save_message(str(response), MessageType.AI_MESSAGE)



if __name__ == "__main__":
    ConversationalChatModel().start_coversation()
