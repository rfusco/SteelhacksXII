from dataclasses import dataclass, field
from typing import List, Optional
from bson import ObjectId
from datetime import datetime


# -----------------------------
# Sentence
# -----------------------------
@dataclass
class Sentence:
    """
    Represents a single sentence spoken by a person in a conversation.

    Attributes:
        speaker (ObjectId): Reference to the Person._id who spoke this sentence.
        text (str): The text content of the sentence.
        sentiment (str): Sentiment label of the sentence (e.g., 'positive', 'negative').
        start_time (Optional[datetime]): Timestamp when the sentence started.
        total_time (int): Duration of the sentence in seconds.
        _id (ObjectId): Unique identifier for the sentence.
    """
    speaker: ObjectId
    text: str
    sentiment: str
    start_time: Optional[datetime] = None
    total_time: int = 0
    _id: ObjectId = field(default_factory=ObjectId)

    @classmethod
    def from_dict(cls, data: dict) -> "Sentence":
        """
        Creates a Sentence object from a MongoDB document.

        Args:
            data (dict): MongoDB document representing a sentence.

        Returns:
            Sentence: A Python Sentence object.
        """
        return cls(
            _id=data.get("_id", ObjectId()),
            speaker=data.get("speaker"),
            text=data.get("text", ""),
            sentiment=data.get("sentiment", ""),
            start_time=data.get("start_time"),
            total_time=data.get("total_time", 0)
        )

    def to_dict(self) -> dict:
        """
        Converts the Sentence object to a dictionary suitable for MongoDB insertion.

        Returns:
            dict: MongoDB-ready dictionary representing the sentence.
        """
        return {
            "_id": self._id,
            "speaker": self.speaker,
            "text": self.text,
            "sentiment": self.sentiment,
            "start_time": self.start_time,
            "total_time": self.total_time
        }


# -----------------------------
# Conversation
# -----------------------------
@dataclass
class Conversation:
    """
    Represents a conversation consisting of multiple sentences and participants.

    Attributes:
        participants (List[ObjectId]): List of Person._id participating in the conversation.
        start_time (datetime): Timestamp when the conversation started.
        total_time (int): Duration of the conversation in seconds.
        sentences (List[Sentence]): List of Sentence objects in the conversation.
        flags (List[ObjectId]): List of sentence IDs that were flagged.
        sentiment (str): Overall sentiment of the conversation.
        _id (ObjectId): Unique identifier for the conversation.
    """
    participants: List[ObjectId]
    start_time: datetime
    total_time: int = 0
    sentences: List[Sentence] = field(default_factory=list)
    flags: List[ObjectId] = field(default_factory=list)
    sentiment: str = ""
    _id: ObjectId = field(default_factory=ObjectId)

    @classmethod
    def from_dict(cls, data: dict) -> "Conversation":
        """
        Creates a Conversation object from a MongoDB document.

        Args:
            data (dict): MongoDB document representing a conversation.

        Returns:
            Conversation: A Python Conversation object.
        """
        return cls(
            _id=data.get("_id", ObjectId()),
            start_time=data.get("start_time"),
            total_time=data.get("total_time", 0),
            participants=data.get("participants", []),
            sentences=[Sentence.from_dict(s) for s in data.get("sentences", [])],
            flags=data.get("flags", []),
            sentiment=data.get("sentiment", "")
        )

    def to_dict(self) -> dict:
        """
        Converts the Conversation object to a dictionary suitable for MongoDB insertion.

        Returns:
            dict: MongoDB-ready dictionary representing the conversation.
        """
        return {
            "_id": self._id,
            "start_time": self.start_time,
            "total_time": self.total_time,
            "participants": self.participants,
            "sentences": [s.to_dict() for s in self.sentences],
            "flags": self.flags,
            "sentiment": self.sentiment
        }


# -----------------------------
# Person
# -----------------------------
@dataclass
class Person:
    """
    Represents a person in the system.

    Attributes:
        name (str): Name of the person.
        role (str): Role of the person (e.g., 'Elder', 'Caregiver').
        conversations (List[ObjectId]): List of Conversation._id the person participates in.
        _id (ObjectId): Unique identifier for the person.
    """
    name: str
    role: str
    conversations: List[ObjectId] = field(default_factory=list)
    _id: ObjectId = field(default_factory=ObjectId)

    @classmethod
    def from_dict(cls, data: dict) -> "Person":
        """
        Creates a Person object from a MongoDB document.

        Args:
            data (dict): MongoDB document representing a person.

        Returns:
            Person: A Python Person object.
        """
        return cls(
            _id=data.get("_id", ObjectId()),
            name=data.get("name", ""),
            role=data.get("role", ""),
            conversations=data.get("conversations", [])
        )

    def to_dict(self) -> dict:
        """
        Converts the Person object to a dictionary suitable for MongoDB insertion.

        Returns:
            dict: MongoDB-ready dictionary representing the person.
        """
        return {
            "_id": self._id,
            "name": self.name,
            "role": self.role,
            "conversations": self.conversations
        }
