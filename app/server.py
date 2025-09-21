from flask import Flask, jsonify
from flask_cors import CORS
from handle_data import (
    get_all_conversations,
    get_all_people,
    get_person_by_name,
    get_conversations_by_person,  # not used anymore, but leaving import
    add_conversation, update_person_conversations_by_id
)
from parse import srt_to_conversation_rnbrad, srt_text

app = Flask(__name__)
CORS(app)

def count_flags_for_person(person_name: str) -> int:
    person = get_person_by_name(person_name)
    if not person:
        return -1  # person not found

    # Get conversation IDs stored on this person
    conversation_ids = person.get("conversations", [])
    
    # Pull all conversations and filter by those IDs
    all_conversations = get_all_conversations()
    person_conversations = [
        conv for conv in all_conversations
        if str(conv.get("_id")) in [str(cid) for cid in conversation_ids]
    ]

    # Count flags
    total_flags = sum(len(conv.get("flags", [])) for conv in person_conversations)
    return total_flags

@app.route('/new-audio')
def handle():
    # process audio and return srt as string
    
    # parse string and store conversation in db
    conversation = srt_to_conversation_rnbrad(srt_text)
    success = add_conversation(conversation)

    # add conversation to all participants
    for participant in conversation.participants:
        update_person_conversations_by_id(participant, conversation._id)
    
    if(success):   return f"Conversation file successfully added", 200
    else: return "Error uploading conversation file"

# /people endpoint to return all people and data attached directly to their objects (name, role, conversations)
@app.route('/people')
def people():
    return get_all_people()

# /conversations endpoint to return all conversations and data attached directly to their objects (participants, sentences, flags)
@app.route('/conversations')
def conversations():
    return get_all_conversations()

# /person/<person_name> endpoint to return a single person by name
@app.route('/person/<person_name>')
def person_detail(person_name):
    return get_person_by_name(person_name) 

# /conversation/<conv_id> endpoint to return a single conversation by ID
@app.route('/conversation/<conv_id>')
def conversation_detail(conv_id):
    # fetch one conversation by ID
    conv = next((c for c in get_all_conversations() if str(c.get("_id")) == conv_id), None)
    if not conv:
        return jsonify({"error": f"Conversation '{conv_id}' not found"}), 404
    return jsonify(conv)

# /conversations/<person_name> endpoint to return all conversations for a given person
@app.route('/conversations/<person_name>')
def conversations_by_person(person_name):
    return get_conversations_by_person(person_name)

# /flags/<person_name> endpoint to return total number of flags across all conversations for a given person
@app.route('/flags/<person_name>', methods=['GET'])
def flags_endpoint(person_name):
    total_flags = count_flags_for_person(person_name)

    if total_flags == -1:
        return jsonify({"error": f"Person '{person_name}' not found"}), 404

    return jsonify({"person": person_name, "total_flags": total_flags})


if __name__ == '__main__':
    app.run(debug=True)