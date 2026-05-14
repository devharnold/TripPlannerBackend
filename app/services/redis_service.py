import redis
import json
import os
from typing import Any, Optional
from datetime import datetime

# Set up redis client
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=os.getenv("REDIS_PORT"),
    decode_responses=True
)

# Set 1 hour cache expiry, travel prices mutate after short while
CACHE_EXPIRY = int(os.getenv("CACHE_EXPIRY", 3600))

# Helper Function
def build_cache_key(category: str, user_id: str, *args) -> str:
    """
    Generates consistent redis keys

    Example:
    flights:user123:nbo:dbi
    hotel:user123:dbi
    """
    key_parts = [category, user_id]
    for arg in args:
        if arg:
            key_parts.append(str(arg).lower())

    return ":".join(key_parts)

# Cache setter: This is Generic
def set_cache(key: str, data: Any, expiry: int = CACHE_EXPIRY) -> bool:
    """Stores data in redis with expiry"""
    try:
        redis_client.setex(key, expiry, json.dumps(data))
        return True
    except redis.RedisError as e:
        print(f"[Redis SET Error] {e}")
        return False
    
# Cache Getter
def get_cache(key: str) -> Optional[Any]:
    """Fetches data from Redis"""
    try:
        data = redis_client.get(key)
        if not data:
            return None
        return json.loads(data)
    
    except redis.RedisError as e:
        print(f"[Redis GET Error] {e}")
        return None
    
    except json.JSONDecodeError as e:
        print(f"[JSON DECODE Error] {e}")
        return None
    
# Cache Delete
def delete_cache(key: str) -> bool:
    """Deletes a cache key"""
    try:
        redis_client.delete(key)
        return True
    except redis.RedisError as e:
        print(f"[Redis DELETE Error] {e}")
        return False
    
# Flight Cache Functions
def cache_flights(user_id: str, origin: str, destination: str, data: dict) -> bool:
    key = build_cache_key("flights", user_id, origin, destination)
    return set_cache(key, data)

def get_cached_flights(user_id: str, origin: str, destination: str):
    key = build_cache_key("flights", user_id, origin, destination)
    return get_cache(key)

# AirBnB Cache Functions
def cache_bnbs(user_id: str, city: str, checkin_date: datetime, data: dict) -> bool:
    key = build_cache_key("bnbs", user_id, city, checkin_date)
    return set_cache(key, data)

def get_cached_bnbs(user_id: str, city: str, checkin_date: datetime):
    key = build_cache_key("bnbs", user_id, city, checkin_date)
    return get_cache(key)

# Hotel Cache Functions
def cache_hotels(user_id: str, city: str, data: dict):
    key = build_cache_key("hotels", user_id, city)
    return set_cache(key, data)

def get_cached_hotels(user_id: str, city: str):
    key = build_cache_key("hotels", user_id, city)
    return get_cache(key)

# Itineraries Cache Functions
def cache_itenirary(user_id: str, destination: str, data: dict):
    key = build_cache_key("itinerary", user_id, destination)
    return set_cache(key, data)

def get_cached_iteneraries(user_id: str, destination: str):
    key = build_cache_key("itinerary", user_id, destination)
    return get_cache(key)

# Budget Cache Functions
def cache_budget(user_id: str, destination: str, data: dict) -> bool:
    key = build_cache_key("budget", user_id, destination, data)
    return set_cache(key, data)

def get_cached_budget(user_id: str, destination: str):
    key = build_cache_key("budget", user_id, destination)
    return get_cache(key)

# Session State Cache
def cache_workflow_state(session_id: str, state_data: dict) -> bool:
    """
    This stores workflow states for the agents
    Comes in handy in long-running sessions
    """
    key = build_cache_key("workflow_state", session_id)
    return set_cache(key, state_data, expiry=2700)

def get_cached_workflow_state(session_id: str):
    key = build_cache_key("workflow_state", session_id)
    return get_cache(key)

# Health Check
def redis_health_check() -> bool:
    try:
        redis_client.ping()
        return True
    
    except redis.RedisError as e:
        print(f"[Redis Health Error] {e}")
        return False