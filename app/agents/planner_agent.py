import os
from typing import Dict, Any

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage


# Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.3
)

# System Prompt
SYSTEM_PROMPT = """
You are an AI Travel Planner.

Your responsibilities:
- Understand the user's travel goals
- Create optimized travel plans
- Determine which specialized agents should be used
- Respect budget constraints
- Ask for missing details when necessary

Available Agents:
1. flight_agent
   - Finds flights
   - Compares prices
   - Suggests cheapest routes

2. hotel_agent
   - Finds hotels
   - Suggests accommodation

3. activity_agent
   - Suggests activities and attractions

4. budget_agent
   - Estimates trip costs

Rules:
- Be concise
- Return structured responses
- If information is missing, request it
"""


# Planner Agent
class PlannerAgent:
    async def run(self, user_prompt: str) -> Dict[str, Any]:
        response = await llm.ainvoke([
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=user_prompt)
        ])

        return {"status": "success", "response": response.content}