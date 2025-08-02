from typing import List
from langchain_redis import RedisChatMessageHistory

class ChatMessagePersistance :
    def main(self, messages: List) :
        print(messages)

if __name__ == "__main__" :
    persistance = ChatMessagePersistance()
    persistance.main(["Hello World"])
