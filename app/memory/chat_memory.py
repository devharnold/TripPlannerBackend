import json
from typing import List, Dict

from app.services.redis_service import redis_client

CHAT_HISTORY_TTL = 60 * 60 * 24

class ChatMemory:
    @staticmethod
    async def add_message(user_id: str, role: str, content: str):
        key = f"chat_history: {user_id}"
        message = {"role": role, "content": content}

        existing_messages = await redis_client.get(key)
        if existing_messages:
            messages = json.loads(existing_messages)
        else:
            messages = []

        messages.append(message)

        await redis_client.set(key, json.dumps(messages), ex=CHAT_HISTORY_TTL)

    @staticmethod
    async def get_history(user_id: str) -> List[Dict]:
        key = f"chat_history: {user_id}"
        data = await redis_client.get(key)
        if not data:
            return []
        return json.loads(data)
    
    @staticmethod
    async def clear_history(user_id: str):
        key = f"chat_history: {user_id}"
        await redis_client.delete(key)