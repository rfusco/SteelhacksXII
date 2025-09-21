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

def add_conversation(conversation: Conversation) -> bool:
    """Add the conversation to the database.

    Args:
        conversation (Conversation): The conversation to add

    Returns:
        Success of the addition
    """
    return conversations.insert_one(conversation.to_dict()).inserted_id is not None


def add_person(person: Person) -> bool:
    """
    Add the person to the database.

    Args:
        person (Person): The person to add

    Returns:
        Success of the addition
    """
    people.insert_one(person.to_dict()).inserted_id is not None

def update_person_name(person_id: str, name: str) -> bool:
    """
    Updates the name of the person specified by id.

    Args:
        person_id (str): The ObjectId of the person as a string.
        name (str): The new name to set.

    Returns:
        bool: True if a document was updated, False otherwise.
    """
    return people.update_one({"_id": ObjectId(person_id)}, {"$set": {"name": name}}).modified_count > 0

def update_person_role_by_id(person_id: str, role: str) -> bool:
    """
    Updates the role of the person specified by id.

    Args:
        person_id (str): The ObjectId of the person as a string.
        role (str): The new role to set.

    Returns:
        bool: True if a document was updated, False otherwise.
    """
    return people.update_one({"_id": ObjectId(person_id)}, {"$set": {"role": role}}).modified_count > 0

def update_person_role_by_name(name: str, role: str) -> bool:
    """
    Updates the role of the person specified by name.

    Args:
        name (str): The name of the person as a string.
        role (str): The new role to set.

    Returns:
        bool: True if a document was updated, False otherwise.
    """
    return people.update_one({"name": name}, {"$set": {"role": role}}).modified_count > 0

def update_person_conversations_by_name(name: str, convoid: str) -> bool:
    """
    Updates the conversations of the person specified by name by adding a new conversation ID.

    Args:
        name (str): The name of the person whose conversations should be updated.
        convoid (str): The ObjectId (as string) of the conversation to add.

    Returns:
        bool: True if the conversation ID was added or updated, False otherwise.
    """
    result = people.update_one(
        {"name": name},
        {"$addToSet": {"conversations": ObjectId(convoid)}}
    )
    # $addToSet ensures we don't add duplicates
    return result.modified_count > 0

def update_person_conversations_by_id(person_id: str, convoid: str) -> bool:
    """
    Updates the conversations of the person specified by ObjectId by adding a new conversation ID.

    Args:
        person_id (str): The ObjectId of the person as a string.
        convoid (str): The ObjectId (as string) of the conversation to add.

    Returns:
        bool: True if the conversation ID was added or updated, False otherwise.
    """
    result = people.update_one(
        {"_id": ObjectId(person_id)},
        {"$addToSet": {"conversations": ObjectId(convoid)}}
    )
    # $addToSet ensures we don't add duplicates
    return result.modified_count > 0
