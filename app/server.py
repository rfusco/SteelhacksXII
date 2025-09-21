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
    conversation = srt_to_conversation_rnbrad(srt_text="""1
00:00:00,000 --> 00:00:03,000
Speaker 0: Could you please help me get up?

2
00:00:03,200 --> 00:00:05,000
Speaker 1: Ugh, not again. You're always asking for help.

3
00:00:05,200 --> 00:00:08,000
Speaker 0: My leg hurts. I need the medicine you promised.

4
00:00:08,200 --> 00:00:10,000
Speaker 1: You forget everything. I don't have time to babysit you.

5
00:00:10,200 --> 00:00:13,400
Speaker 0: I'm cold. Could you close the window and bring a blanket?

6
00:00:13,600 --> 00:00:16,000
Speaker 1: Fine. If you complain one more time I'm not covering you.

7
00:00:16,200 --> 00:00:19,000
Speaker 0: Yesterday you said you'd call the doctor about my test results.

8
00:00:19,200 --> 00:00:21,000
Speaker 1: I told you already — it's not urgent. Stop worrying and shut up.

9
00:00:21,200 --> 00:00:24,000
Speaker 0: I'm hungry. Can I have something to eat?

10
00:00:24,200 --> 00:00:26,000
Speaker 1: There's nothing good left. Eat what's there or don't eat.
11
00:00:26,200 --> 00:00:29,000
Speaker 0: I'm scared when you talk to me like that.

12
00:00:29,200 --> 00:00:31,000
Speaker 1: Well maybe you should stop being so needy. I'm tired of this burden.

13
00:00:31,200 --> 00:00:34,000
Speaker 0: You promised not to let me be alone at night.

14
00:00:34,200 --> 00:00:36,000
Speaker 1: Promised? I promised a lot of things. Not my problem anymore.

15
00:00:36,200 --> 00:00:39,000
Speaker 0: Please — the bathroom is hard for me. I can't stand long.

16
00:00:39,200 --> 00:00:41,000
Speaker 1: Urge it then. I can't drop everything for you every time.

17
00:00:41,200 --> 00:00:44,000
Speaker 0: I feel so alone when you speak to me like this.

18
00:00:44,200 --> 00:00:46,000
Speaker 1: Everyone would be better off without the extra trouble you cause.

19
00:00:46,200 --> 00:00:48,000
Speaker 0: That hurts. Why would you say that?

20
00:00:48,200 --> 00:00:52,000
Speaker 1: Because it's true. You're wasting my time and money. Stop being dramatic.

21
00:00:52,200 --> 00:00:55,000
Speaker 0: I just want to be treated with respect.

22
00:00:55,200 --> 00:00:58,000
Speaker 1: Respect is earned. You make it impossible.

23
00:00:58,200 --> 00:01:02,000
Speaker 0: Please let me call my daughter.

24
00:01:02,200 --> 00:01:04,000
Speaker 1: Call her yourself. I told you the phone line is for emergencies not for whining.""")
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