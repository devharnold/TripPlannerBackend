import json
from datetime import datetime
from typing import Dict, Any

from pydantic import BaseModel, ValidationError
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

from app.tools.hotel_search import search_hotels

# Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="",
    temparature=0.2
)

class HotelSearchSchema(BaseModel):
    origin: str
    destination: str
    