from enum import Enum


class MessageType(Enum):
    SYSTEM_MESSAGE = "SYSTEM_MESSAGE",
    AI_MESSAGE = "AI_MESSAGE",
    USER_MESSAGE = "USER_MESSAGE"
