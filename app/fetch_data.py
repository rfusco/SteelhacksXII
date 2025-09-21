# fetch_data.py
from dotenv import load_dotenv
import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
from datetime import datetime
import json
from models import Person, Conversation, Sentence

load_dotenv()

# -----------------------------
# MongoDB Connection
# -----------------------------
uri = os.getenv("MONGO_DB_KEY")
client = MongoClient(uri, server_api=ServerApi('1'))

db = client["ElderData"]
people = db["People"]
conversations = db["Conversations"]

# -----------------------------
# Helper for JSON-safe conversion
# -----------------------------
def json_safe(obj):
    """Convert ObjectId and datetime to JSON-serializable formats."""
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def serialize_person(person: Person) -> dict:
    """Return JSON-serializable dict for a Person object."""
    d = person.to_dict()
    d["_id"] = str(d["_id"])
    d["conversations"] = [str(c) for c in d["conversations"]]
    return d

def serialize_conversation(convo: Conversation) -> dict:
    """Return JSON-serializable dict for a Conversation object."""
    d = convo.to_dict()
    d["_id"] = str(d["_id"])
    d["participants"] = [str(p) for p in d["participants"]]
    d["flags"] = [str(f) for f in d["flags"]]
    # sentences
    for i, s in enumerate(d["sentences"]):
        d["sentences"][i]["_id"] = str(s["_id"])
        d["sentences"][i]["speaker"] = str(s["speaker"])
        if s["start_time"]:
            d["sentences"][i]["start_time"] = s["start_time"].isoformat()
    return d

# -----------------------------
# Fetch Functions
# -----------------------------
def get_all_people():
    """Return list of all people as JSON-serializable dicts."""
    people_docs = people.find()
    return [serialize_person(Person.from_dict(p)) for p in people_docs]

def get_person_by_name(name: str):
    """Return a single person by name as JSON-serializable dicts.."""
    p_doc = people.find_one({"name": name})
    if not p_doc:
        return None
    return serialize_person(Person.from_dict(p_doc))

def get_all_conversations():
    """Return all conversations as JSON-serializable dicts."""
    convo_docs = conversations.find()
    return [serialize_conversation(Conversation.from_dict(c)) for c in convo_docs]

def get_conversations_by_person(name: str):
    """
    Return all conversations that a person participates in,
    using the conversation IDs stored in their Person document as JSON-serializable dicts.
    """
    # 1. Find the person document by name
    person_doc = people.find_one({"name": name})
    if not person_doc:
        return []

    # 2. Extract conversation IDs
    convo_ids = [ObjectId(c) for c in person_doc.get("conversations", [])]

    if not convo_ids:
        return []

    # 3. Fetch conversations by their IDs
    convo_docs = conversations.find({"_id": {"$in": convo_ids}})

    # 4. Serialize to JSON-safe dicts
    return [serialize_conversation(Conversation.from_dict(c)) for c in convo_docs]

