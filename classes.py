import uuid

class Person:
    def __init__(self, name, role, conversations: list[Conversation]): # type: ignore
        self.GUID = uuid.uuid4
        self.name = name
        self.role = role
        self.conversations = conversations
    name = None
    role = None
    GUID = None
    conversations = None #Conversation Array

class Sentence:
    def __init__(self, startTime, duration, text, speaker: Person, sentiment):
        pass
    startTime = None
    duration = None
    text = None
    speaker = None #Person Object
    sentiment = None

class Conversation:
    def __init__(self, startTime, duration, participants: list[Person], sentences: list[Sentence], sentiment, flags):
        self.startTime = startTime
        self.duration = duration
        self.participants = participants
        self.sentences = sentences
        self.sentiment = sentiment
        self.flags = flags

    startTime = None
    duration = None
    participants = None #Person Array
    sentences = None #Sentence Array
    sentiment = None
    flags = None
    

        