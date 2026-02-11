from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from enum import Enum
import random
from datetime import datetime

app = FastAPI(title="Daily Oracle 🍀✨")

# -----------------------------
# Models
# -----------------------------
class Weekday(str, Enum):
    monday = "monday"
    tuesday = "tuesday"
    wednesday = "wednesday"
    thursday = "thursday"
    friday = "friday"
    saturday = "saturday"
    sunday = "sunday"


class QuoteInput(BaseModel):
    quote: str = Field(..., min_length=5, example="Your luck is glowing today ✨")


# -----------------------------
# Data Store (7 Days)
# -----------------------------
weekly_oracle = {
    "monday": [
        "Monday tried to ruin your vibe… but you’re built different 😼☕",
        "New week, new chaos, same main character energy ✨"
    ],
    "tuesday": [
        "Tuesday luck is quietly building up… stay cute 🍀",
        "You’re doing better than you think 💖"
    ],
    "wednesday": [
        "Midweek check: you’re still iconic 💅",
        "Halfway through… don’t stop glowing ✨"
    ],
    "thursday": [
        "Thursday is basically Friday’s hot friend 😌",
        "Your luck is warming up… get ready 🍀"
    ],
    "friday": [
        "Friday luck is LEGENDARY. Go flirt with life 😼✨",
        "Weekend energy is already chasing you 💖"
    ],
    "saturday": [
        "Saturday is for rest, romance, and random blessings 🌙",
        "Luck is high. Do something fun ✨"
    ],
    "sunday": [
        "Sunday is soft. Recharge your magic 💖",
        "The universe is proud of you. Take it slow 🍀"
    ]
}

luck_levels = ["LOW 😴", "MEDIUM 🌿", "HIGH 🍀", "EPIC 🔥", "LEGENDARY ✨😼"]


# =====================================================
# ADMIN ENDPOINTS (CRUD for Quotes)
# =====================================================

# Create Quote
@app.post("/weekly/{day}")
def add_quote(day: Weekday, input_data: QuoteInput):
    weekly_oracle[day.value].append(input_data.quote)
    return {
        "message": f"Added new quote to {day.value} ✅",
        "total_quotes": len(weekly_oracle[day.value]),
        "quotes": weekly_oracle[day.value]
    }


# Update Quote
@app.put("/weekly/{day}/{index}")
def update_quote(day: Weekday, index: int, input_data: QuoteInput):
    quotes = weekly_oracle[day.value]

    if 0 <= index < len(quotes):
        quotes[index] = input_data.quote
        return {
            "message": "Quote updated ✨",
            "updated_quote": quotes[index]
        }

    raise HTTPException(status_code=404, detail="Quote index out of range")


# Delete Quote
@app.delete("/weekly/{day}/{index}")
def delete_quote(day: Weekday, index: int):
    quotes = weekly_oracle[day.value]

    if len(quotes) <= 1:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete the last quote! Oracle must speak 😭"
        )

    if 0 <= index < len(quotes):
        removed = quotes.pop(index)
        return {
            "message": f"Deleted quote",
            "removed": removed,
            "remaining_quotes": len(quotes)
        }

    raise HTTPException(status_code=404, detail="Quote index out of range")


# Read All Quotes for a Day (Admin View)
@app.get("/weekly/{day}")
def get_all_quotes(day: Weekday):
    return {
        "day": day.value,
        "total": len(weekly_oracle[day.value]),
        "quotes": weekly_oracle[day.value]
    }


# =====================================================
# USER ENDPOINTS (Random Predictions)
# =====================================================

# Oracle Today (IMPORTANT: put above /oracle/{day})
@app.get("/oracle/today")
def oracle_today():
    today = datetime.today().strftime("%A").lower()

    quotes = weekly_oracle.get(today, weekly_oracle["monday"])

    return {
        "day": today,
        "luck_level": random.choice(luck_levels),
        "prediction": random.choice(quotes)
    }


# Oracle for Any Day (User chooses)
@app.get("/oracle/{day}")
def oracle_by_day(day: Weekday):
    quotes = weekly_oracle[day.value]

    return {
        "day": day.value,
        "luck_level": random.choice(luck_levels),
        "prediction": random.choice(quotes)
    }
