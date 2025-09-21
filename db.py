from dotenv import load_dotenv
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
from models import Person, Conversation, Sentence  # import your classes


###
# TESTING CONNECTION AND STUFF SEE THIS FOR HOW IT WORKS. SEE MODELS.PY TOO
###

# =============================
# Database Connection
# =============================

load_dotenv()
uri = os.getenv("MONGO_DB_KEY")
client = MongoClient(uri, server_api=ServerApi('1'))

db = client["ElderData"]
people = db["People"]
conversations = db["Conversations"]


# =============================
# Usage Example
# =============================

# 1. Insert a new Person
alice = Person(name="Alice", role="Elder", conversations=[])
people.insert_one(alice.to_dict())
print("Inserted Person:", alice.to_dict())

# 2. Create a Conversation where Alice speaks
sentence1 = Sentence(speaker=alice._id, text="Hello, I feel unsafe.", sentiment="",
                     start_time=datetime.now(), total_time=3)
sentence2 = Sentence(speaker=alice._id, text="Can someone help me?", sentiment="",
                     start_time=datetime.now(), total_time=4)

conversation = Conversation(
    participants=[alice._id],
    sentences=[sentence1, sentence2],
    start_time=datetime.now(),
    total_time=7,
    sentiment="",
    flags=[]
)

conversations.insert_one(conversation.to_dict())
print("Inserted Conversation:", conversation.to_dict())

# 3. Link conversation back to Alice
people.update_one(
    {"_id": alice._id},
    {"$push": {"conversations": conversation._id}}
)

# 4. Query Alice back and show her conversations
alice_doc = people.find_one({"name": "Alice"})
alice_obj = Person.from_dict(alice_doc)
print("Alice (from DB):", alice_obj.to_dict())

# 5. Get Alice’s conversations and her sentences
for convo_doc in conversations.find({"participants": alice._id}):
    convo_obj = Conversation.from_dict(convo_doc)
    print("Conversation found:", convo_obj.to_dict())

    # Get Alice's sentences
    alice_sentences = [s.text for s in convo_obj.sentences if s.speaker == alice._id]
    print("Alice's sentences:", alice_sentences)

# 6. Update Alice’s role and push back
people.replace_one({"_id": alice_obj._id}, alice_obj.to_dict())
print("Updated Alice:", people.find_one({"_id": alice_obj._id}))
