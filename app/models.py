# FastAPI pydantic models

from pydantic import BaseModel, Field, EmailStr
from datetime import date, datetime
from typing import List, Optional, Literal
from decimal import Decimal
from enum import Enum

# Google AUTH Request
class GoogleAuthRequest(BaseModel):
    token: str

#Shared across services
class Currency(str, Enum):
    USD = "USD"
    GBP = "GBP"
    KES = "KES"

class BookingItemType(str, Enum):
    FLIGHT = "flight"
    HOTEL = "hotel"
    ACTIVITY = "activity"

class BookingState(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    FAILED = "failed"

# Abstract Money
class Money(BaseModel):
    amount: Decimal
    currency: Currency


# User Personalization
class UserPreferences(BaseModel):
    budget_range: Optional[Literal["low", "medium", "high"]] = None
    travel_style: Optional[Literal["luxury", "budget", "balanced"]] = "balanced"
    interests: List[str] = []
    preferred_climate: Optional[str] = None
    pace: Optional[Literal["relaxed", "moderate", "fast"]] = "moderate"

class UserProfile(BaseModel):
    user_id: str
    email: EmailStr
    preferences: UserPreferences

#Trip Input (Core)
class TripRequest(BaseModel):
    user_id: str
    origin: str
    destination: str
    start_date: date
    end_date: date
    budget: float
    travelers: int = Field(gt=0)
    preferences: Optional[UserPreferences] = None # depends on the users preferences
    additional_prompt: Optional[str] = None

# Recommendation Engine
class Activity(BaseModel):
    name: str
    description: Optional[str] = None
    location: str
    estimated_cost: float
    duration_hours: float

class DayPlan(BaseModel):
    day: int
    activities: List[Activity]

class RecommendationScore(BaseModel):
    relevance: float = Field(ge=0, le=1)
    personalization_score: float = Field(ge=0, le=1)

class TripPlan(BaseModel):
    trip_id: str
    destination: str
    total_estimated_cost: float
    itenerary: List[DayPlan]
    score: RecommendationScore

# Suggestions these are: Multiple Options
class TripSuggestion(BaseModel):
    suggestion_id: str
    destination: str
    estimated_cost: float
    highlights: List[str]
    score: RecommendationScore

class SuggestionResponse(BaseModel):
    user_id: str
    suggestions: List[TripSuggestion]
    generated_at: datetime

# Autonomous Booking: Future Integration With Golang(Accept multiple currencies)
class BookingItem(BaseModel):
    type: BookingItemType
    provider: str
    reference_id: Optional[str] = None
    price: Money

class BookingRequest(BaseModel):
    trip_id: str
    user_id: str
    items: List[BookingItem]

# Wrote a BookingStatus one
class BookingStatus(BaseModel):
    booking_id: str
    status: BookingState
    items: List[BookingItem]
    total_converted: Optional[Money] = None

    conversion_rate: Optional[Decimal] = None
    base_currency: Optional[Currency] = None

    created_at: datetime
    updated_at: Optional[datetime] = None

# Autonomous Payments
class PaymentMethod(BaseModel):
    method_id: str
    type: Literal["card", "wallet", "bank"]
    provider: str
    last4: Optional[str] = None

class PaymentAuthorization(BaseModel):
    user_id: str
    trip_id: str
    max_amount: float
    currency: Optional[Currency]
    approved: bool = False

class PaymentTransaction(BaseModel):
    transaction_id: str
    booking_id: str
    amount: float
    currency: str
    status: Literal["initiated", "authorized", "completed", "failed"]
    timestamp: datetime

#API Responses
class APIResponse(BaseModel):
    success: bool
    message: str

class TripPlanResponse(APIResponse):
    data: TripPlan

class BookingRequestResponse(APIResponse):
    data: BookingStatus

class PaymentResponse(APIResponse):
    data: PaymentTransaction