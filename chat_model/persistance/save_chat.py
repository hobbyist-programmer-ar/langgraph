import logging
import os
import traceback

from langchain_core.messages.system import SystemMessage
from langchain_redis import RedisChatMessageHistory

from chat_model.message_type import MessageType

# Logging Configurations
logging.basicConfig(level=os.getenv("LOGGING_LEVEL", logging.INFO))

# Redis Configurations
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
print(f"Connecting to Redis at: {REDIS_URL}")
history = RedisChatMessageHistory(session_id="chat_history", redis_url=REDIS_URL)

class ChatMessagePersistance :
    def save_message(self, messages: str, message_type: MessageType) :
        if message_type is MessageType.SYSTEM_MESSAGE:
            self.save_system_message(messages)
        elif message_type is MessageType.USER_MESSAGE:
            self.save_user_message(messages)
        else:
            self.save_ai_message(messages)

    def save_system_message(self, message: str):
        try:
            history.add_message(SystemMessage(content=message))
        except Exception:
            logging.info("Exception Occured while saving message to" +
                f"Redis cache : {traceback.print_exc()}")
        else:
            logging.info(f"System Message : {message} stored in the Redis Cache")

    def save_user_message(self, message: str):
        try:
            history.add_user_message(message)
        except Exception:
            logging.info("Exception Occured while saving message to" +
                f"Redis cache : {traceback.print_exc()}")
        else:
            logging.info(f"User Message : {message} stored in the Redis Cache")

    def save_ai_message(self, message: str):
        try:
            history.add_ai_message(message)
        except Exception:
            logging.info("Exception Occured while saving message to" +
                f"Redis cache : {traceback.print_exc()}")
        else:
            logging.info(f"AI Message : {message} stored in the Redis Cache")

if __name__ == "__main__" :
    persistance = ChatMessagePersistance()
    persistance.save_message("Hello World", MessageType.SYSTEM_MESSAGE)
