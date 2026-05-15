from typing import List

from pydantic import BaseModel


# -----------------------------------
# Incoming Message
# -----------------------------------

class Message(BaseModel):

    role: str
    content: str


# -----------------------------------
# Chat Request
# -----------------------------------

class ChatRequest(BaseModel):

    messages: List[Message]


# -----------------------------------
# Recommendation Object
# -----------------------------------

class Recommendation(BaseModel):

    name: str
    url: str
    test_type: str


# -----------------------------------
# Chat Response
# -----------------------------------

class ChatResponse(BaseModel):

    reply: str

    recommendations: List[Recommendation]

    end_of_conversation: bool